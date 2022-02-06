import xml
import sys
import yaml
import os
import sys

from .gitea import GiteaAPI
from .atom import AtomFeed


feeds = [
    {
        'name':'Gitea',
        'url':'https://github.com/go-gitea/gitea/releases.atom',
        'exclude':['dev', 'rc'],
        'assign':''
    }
]

def load_yaml(_file: str):
    required = ['feeds', 'token', 'url']
    config = {}

    with open(_file, 'r') as f:
        config =  yaml.load(f.read(), Loader=yaml.FullLoader)

    return config

def main():
    #token = sys.argv[1]
    #api = GiteaAPI("https://gitea.my.cum.re", token)
    #api.searchIssue('infra', 'ansible', '', 'update')
    feed = AtomFeed(feeds[0]['url'])
    print(feed.get_latest([]))
