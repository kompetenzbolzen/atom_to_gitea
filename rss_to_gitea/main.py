import xml
import sys
from .gitea import GiteaAPI

def main():
    token = sys.argv[1]
    api = GiteaAPI("https://gitea.my.cum.re", token)
    api.searchIssue('infra', 'ansible', '', 'update')
