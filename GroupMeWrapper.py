import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning, SNIMissingWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)

class GroupMeWrapper:

    def __init__(self):
        self.base_URL = 'https://api.groupme.com/v3'
        self.access_token = '' # This will have to be read from config file given by user.


    def get_groups(self):
        request = requests.get('{}/groups?token={}'.format(self.base_URL, self.access_token))
        return request.json()['response']


    def get_group_messages(self, group_ID):
        request = requests.get('{}/groups/{}/messages?limit=100&token={}'.format(self.base_URL, group_ID, self.access_token))
        response = request.json()['response']
        messages = response['messages']
        all_messages = []
        all_messages += messages

        while (response['count'] != 0):
            before_ID = messages[-1]['id']
            request = requests.get('{}/groups/{}/messages?limit=100&before_id={}&token={}'.format(self.base_URL, group_ID, before_ID, self.access_token))

            if (request.status_code == 304):
                break

            response = request.json()['response']
            messages = response['messages']

            # TODO: Sometimes message return length of 0. I have no idea why. Investigate.
            if (len(messages) == 0):
                continue

            # By default, we don't care about system messages. These are notifications when someone
            # changes their name, the group name, the group topic, etc.
            for message in messages:
                if message['user_id'] != 'system' and message['text']:
                    all_messages.append(message)

        return all_messages

    def get_group_members(self, group_ID):
        request = requests.get('{}/groups/{}?token={}'.format(self.base_URL, group_ID, self.access_token))
        members = request.json()['response']['members']

        members_set = set()
        for member in members:
            members_set.add(member['user_id'])

        return members_set

# Before ID:
# 146958209370182717