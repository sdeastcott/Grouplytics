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
            if group['name'] == group_name:
                return group['id']

         
    def _get_messages(self):
        request = requests.get('{}/groups/{}/messages?limit=100&token={}'.format(self.base_URL, self.group_ID, self.access_token))
        response = request.json()['response']
        messages = response['messages']
        all_messages = []
        all_messages += messages

        while response['count'] != 0:
            before_ID = messages[-1]['id']
            request = requests.get('{}/groups/{}/messages?limit=100&before_id={}&token={}'
                                   .format(self.base_URL, self.group_ID, before_ID, self.access_token))

	    # TODO: 
            # If no messages are found (e.g. when filtering with before_id) we return code 304. 
            # Not sure how this can ever happen with the while loop predicate
            if (request.status_code == 304): break
            response = request.json()['response']
            messages = response['messages']

            # TODO: 
            # You would think status code 304 would get raised if this were the case, but it
            # has happened. Needs further investigation.
            if (len(messages) == 0): continue

            # By default, we don't care about system messages. These are notifications when
            # someone changes their name, the group name, the group topic, etc.
            for message in messages:
                if message['user_id'] != 'system' and message['text']:
                    all_messages.append(message)

        return all_messages


    # TODO: 
    # This is quite possibly the most convoluted function in the world. 
    # Will come back and clean up.
    def _get_members(self, members_from_file):
        request = requests.get('{}/groups/{}?token={}'.format(self.base_URL, self.group_ID, self.access_token))
        members_from_response = request.json()['response']['members']
        
        name_and_nickname = {}
        for member in members_from_file:
            member = member.split(':')
            name_and_nickname[member[0]] = member[1]

        name_and_ID = {}
        for member in members_from_response:
            for name, nickname in name_and_nickname.items():
                if member['nickname'] == nickname:
                    name_and_ID[name] = member['user_id']

        return name_and_ID
