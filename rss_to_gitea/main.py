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
        return 1

    config = Config(sys.argv[1])
    api = GiteaAPI("https://gitea.my.cum.re", config.token)

    label_id = api.getLabelId(config.owner, config.repo, config.label)

    for feed in config.feeds:
        remote = AtomFeed(feed['url'])
        latest = remote.get_latest(feed['exclude'], feed['include'])

        issue_title = f'{feed["name"]}: {latest["title"]}'
        print("Title=", issue_title)

        ticket = api.searchIssue(config.owner, config.repo, issue_title, [config.label])
        if ticket is not None:
            print(f'{issue_title} already exists. Skipping')
            continue

        result = api.createIssue(config.owner, config.repo, issue_title, '', feed['assign'], [label_id])
