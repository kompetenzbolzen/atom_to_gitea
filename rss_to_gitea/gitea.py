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

    def _api_post(self, _endpoint, _data):
        headers={
                'Authorization':f'token {self.token}',
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        result = requests.post(f'{self.address}/{_endpoint}',headers=headers, json=_data)

        return result.json()

    def _api_patch(self, _endpoint, _data):
        headers={
                'Authorization':f'token {self.token}',
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        result = requests.patch(f'{self.address}/{_endpoint}',headers=headers, json=_data)

        return result.json()


    def createIssue(self, _owner, _repo, _title, _content, _assign, _labels):
        data={
            'assignee':_assign,
            'body':_content,
            'labels':_labels,
            'title':_title
        }

        result = self._api_post(f'repos/{_owner}/{_repo}/issues', data )

        return result

    def changeIssueState(self, _owner, _repo, _index, _state):
        data= {
            'state':_state,
        }

        result = self._api_patch(f'repos/{_owner}/{_repo}/issues/{_index}', data )


    def getFirstExactIssue(self, _owner, _repo, _title, _labels, _state='all'):
        data= {
            'state':_state,
            'labels':_labels,
            'created_by':self.username,
            'q':_title
        }

        result = self._api_get(f'repos/{_owner}/{_repo}/issues', data )

        for issue in result:
            if issue['title'] == _title:
                return issue

        return None

    def getAllIssuesStartingWith(self, _owner, _repo, _title, _labels, _state='all'):
        ret = []

        data= {
            'state':_state,
            'labels':_labels,
            'created_by':self.username,
            'q':_title
        }

        result = self._api_get(f'repos/{_owner}/{_repo}/issues', data )

        for issue in result:
            if issue['title'].startswith(_title):
                ret.append(issue)

        return ret

    def getLabelId(self, _owner, _repo, _label):
        data= {}

        result = self._api_get(f'repos/{_owner}/{_repo}/labels', data )

        label_filtered = filter(lambda a: a['name']==_label, result)
        label = list(label_filtered)

        if len(label) != 1:
            print('No or more than one label found')
            return None

        return label[0]['id']


