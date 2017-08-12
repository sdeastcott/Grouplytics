import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning, SNIMissingWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)


class GroupMe:
    def __init__(self, access_token):
        self._base_URL = 'https://api.groupme.com/v3'
        self._access_token = access_token
    

    def get_group(self, group_id):
        request = requests.get('{}/groups/{}?token={}'.format(self._base_URL, group_id, self._access_token))
        response = request.json()['response']
        return response


    def get_groups(self):
        request = requests.get('{}/groups?token=={}'.format(self._base_URL, self._access_token))
        response = request.json()['response']
        return response


    def get_group_id(self, group_name):
        request = requests.get('{}/groups?token={}'.format(self._base_URL, self._access_token))
        response = request.json()['response']
        for group in response:
            if group_name == group['name']:
                return group['id']


    def get_members(self, group_id):
        request = requests.get('{}/groups/{}?token={}'.format(self._base_URL, group_id, self._access_token))
        members_from_response = request.json()['response']['members']
    
        ID_and_name = {}
        for member in members_from_response:
            ID_and_name[member['user_id']] = member['nickname']

        return ID_and_name

    
    def get_messages(self, group_id, members=None):
        request = requests.get('{}/groups/{}/messages?limit=100&token={}'.format(self._base_URL, group_id, self._access_token))
        response = request.json()['response']
        retrieved = len(response['messages'])
        messages = response['messages']
        message_count = response['count']
        
        while retrieved < message_count:
            before_id = messages[-1]['id']
            request = requests.get('{}/groups/{}/messages?limit=100&before_id={}&token={}'
                                   .format(self._base_URL, group_id, before_id, self._access_token))
            
            # Break if status code 304 (i.e. no data) is returned. TODO: why does this happen?
            if request.status_code == 304: break
            response = request.json()['response']
            retrieved += len(response['messages'])
            messages += response['messages']
            
        if members:
            messages = filter_messages(messages, members)

        return messages


    def filter_messages(self, messages, members):
        messages = []

        for message in messages:
            if message['sender_type'] != 'system' and message['user_id'] in members:
                if message['text']:
                    text = message['text'].strip().lower()
                    text = ''.join(ch for ch in text if ch.isalnum() or ch == " ")
                    message['text'] = text
                messages.append(message)

        return messages