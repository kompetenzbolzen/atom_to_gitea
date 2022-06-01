import xml
import sys
import yaml
import os
import sys

from .gitea import GiteaAPI
from .atom import AtomFeed
from .config import Config

def print_help():
    print('''
USAGE:
    rsstogitea <config>
    ''')

def main():
    if len(sys.argv) <= 1:
        print_help()
        return 1

    config = Config(sys.argv[1])

    token = config.token
    if str.startswith(token, 'env/'):
        splt = token.split('/',1)
        token = os.environ[splt[1]]

    api = GiteaAPI(config.url, token)

    label_id = api.getLabelId(config.owner, config.repo, config.label)

    for feed in config.feeds:
        remote = AtomFeed(feed['url'])
        latest = remote.get_latest(feed['exclude'], feed['include'])

        issue_title = f'{feed["name"]}: {latest["title"]}'
        print("Title=", issue_title)

        ticket = api.getFirstExactIssue(config.owner, config.repo, issue_title, [config.label])
        if ticket is not None:
            print(f'{issue_title} already exists. Skipping')
            continue

        # should we maybe just rename here?
        prev_versions = api.getAllIssuesStartingWith(config.owner, config.repo, f'{feed["name"]}: ', [config.label], _state='open')
        for prev in prev_versions:
            print(f'{prev["title"]} (#{prev["number"]}) already exists. closing.')
            api.changeIssueState(config.owner, config.repo, prev['number'], 'closed')

        result = api.createIssue(config.owner, config.repo, issue_title, latest['link'], feed['assign'], [label_id])
