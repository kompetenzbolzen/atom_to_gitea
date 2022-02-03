import requests
import json

APIBASE="/api/v1"

class GiteaAPIAuthException (Exception):
    pass

class GiteaAPIException (Exception):
    pass

class GiteaAPI:
    def __init__(self, _url, _token):
        self.token = _token
        self.address = _url.strip('/') + APIBASE

        headers={'Authorization':f'token {self.token}'}
        result = requests.get(f'{self.address}/user',headers=headers)

        if result.status_code != 200:
            raise GiteaAPIAuthException(result.json()['message'])

        self.username = result.json()['login']

    def _api_get(self, _endpoint, _params):
        headers={
                'Authorization':f'token {self.token}',
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        result = requests.get(f'{self.address}/{_endpoint}',headers=headers, params=_params)

        return result.json()


    def createIssue(self, _owner, _repo, _title, _content):
        pass

    def searchIssue(self, _owner, _repo, _title, _labels, _state='open'):
        data= {
            'state':_state,
            'labels':_labels,
            'created_by':self.username,
            'q':_title
        }

        result = self._api_get(f'repos/{_owner}/{_repo}/issues', data )

        for issue in result:
            print(issue['title'])

    def updateIssue(self, _owner, _repo, _issueid):
        pass

