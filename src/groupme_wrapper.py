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

    def get_groups(self):
        request = requests.get('{}/groups?token={}'.format(self._base_URL, self._access_token))
        response = request.json()['response']
        return response
