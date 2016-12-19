import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning, SNIMissingWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)


class GroupMeWrapper:
    def __init__(self, access_token, group_name, group_members):
        self.base_URL = 'https://api.groupme.com/v3'
        self.access_token = access_token
        self.group_ID = self._get_group_ID(group_name)
        self.members = self._get_members(group_members)
        self.messages = self._get_messages()

    def _get_group_ID(self, group_name):
        request = requests.get('{}/groups?token={}'.format(self.base_URL, self.access_token))
        response = request.json()['response']
        for group in response:
            # name = ''.join([i if ord(i) < 128 else ' ' for i in group['name']])
            if group_name == group['name']:
                return group['id']

    def _get_messages(self):
        request = requests.get('{}/groups/{}/messages?limit=100&token={}'.format(self.base_URL, self.group_ID, self.access_token))
        response = request.json()['response']
        retrieved = len(response['messages'])
        messages = self._filter_messages(response['messages'])
        message_count = response['count']
        while retrieved != message_count:
            before_ID = messages[-1]['id']
            request = requests.get('{}/groups/{}/messages?limit=100&before_id={}&token={}'
                                   .format(self.base_URL, self.group_ID, before_ID, self.access_token))
             
            # Break if status code 304 (i.e. no data) is returned
            if (request.status_code == 304):
                break
            response = request.json()['response']
            retrieved += len(response['messages'])
            messages += self._filter_messages(response['messages'])

        return messages

    def _filter_messages(self, msgs):
        messages = []
        for message in msgs:
            if message['user_id'] != 'system' and message['user_id'] in self.members:
                messages.append(message)
        return messages

    def _get_members(self, members_from_file):
        request = requests.get('{}/groups/{}?token={}'.format(self.base_URL, self.group_ID, self.access_token))
        members_from_response = request.json()['response']['members']

        name_and_nickname = {}
        for member in members_from_file:
            member = member.split(':')
            name_and_nickname[member[0]] = member[1]

        ID_and_name = {}
        for member in members_from_response:
            for name, nickname in name_and_nickname.items():
                if member['nickname'] == nickname:
                    ID_and_name[member['user_id']] = name

        return ID_and_name
