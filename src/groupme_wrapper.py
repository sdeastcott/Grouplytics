import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning, SNIMissingWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)


class GroupMeWrapper:
    def __init__(self, access_token, group_name):
        self._base_URL = 'https://api.groupme.com/v3'
        self._access_token = access_token
        self._group_data = self._get_group_data(group_name)

    
    def get_group_data(self):
        return self._group_data


    def _get_group_data(self, group_name):
        group_ID = self._get_group_ID(group_name)
        members = self._get_members(group_ID)

        messages = self._get_messages(group_ID, members)
        filtered = self._filter_messages(messages, members)
        user_messages = filtered[0]
        system_messages = filtered[1]
        aliases = self._get_aliases(user_messages, members)

        group_data = {}
        group_data['group_id'] = group_ID
        group_data['members'] = members
        group_data['user_messages'] = user_messages
        group_data['system_messages'] = system_messages
        group_data['creation_date'] = system_messages[-1]['created_at']
        group_data['aliases'] = aliases

        return group_data


    def _get_group_ID(self, group_name):
        request = requests.get('{}/groups?token={}'.format(self._base_URL, self._access_token))
        response = request.json()['response']
        for group in response:
            if group_name == group['name']:
                return group['id']


    def _get_messages(self, group_ID, members):
        request = requests.get('{}/groups/{}/messages?limit=100&token={}'.format(self._base_URL, group_ID, self._access_token))
        response = request.json()['response']
        retrieved = len(response['messages'])
        messages = response['messages']
        message_count = response['count']
        
        while retrieved < message_count:
            before_ID = messages[-1]['id']
            request = requests.get('{}/groups/{}/messages?limit=100&before_id={}&token={}'
                                   .format(self._base_URL, group_ID, before_ID, self._access_token))
            
            # Break if status code 304 (i.e. no data) is returned. TODO: why does this happen?
            if request.status_code == 304: break
            response = request.json()['response']
            retrieved += len(response['messages'])
            messages += response['messages']
            if retrieved % 5000 == 0: print(retrieved)
            
        return messages


    def _filter_messages(self, messages, members):
        user_messages = []
        system_messages = []

        for message in messages:
            if message['sender_type'] == 'system':
                system_messages.append(message)
                continue

            if message['user_id'] in members:
                if message['text']:
                    text = message['text'].strip().lower()
                    text = ''.join(ch for ch in text if ch.isalnum() or ch == " ")
                    message['text'] = text
                user_messages.append(message)

        return (user_messages, system_messages)

    
    def _get_members(self, group_ID):
        request = requests.get('{}/groups/{}?token={}'.format(self._base_URL, group_ID, self._access_token))
        members_from_response = request.json()['response']['members']
    
        ID_and_name = {}
        for member in members_from_response:
            ID_and_name[member['user_id']] = member['nickname']

        return ID_and_name


    def _get_aliases(self, messages, members):
        aliases = {}

        for user_id, nickname in members.items():
            aliases[user_id] = [nickname]

        for message in messages:
            if message['user_id'] in aliases:  
                if message['name'] not in aliases[message['user_id']]:
                    aliases[message['user_id']].append(message['name'])

        return aliases
