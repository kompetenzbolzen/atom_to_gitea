import xml.etree.ElementTree as ET
import requests
import json

from datetime import datetime

def containts_any_of(_str: str, _list: list[str]):
    return True in map(lambda a: a in _str, _list)

def date_compare(date1: str, date2: str):
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    return d1 > d2

def parse_date(date: str):
    '''
    Parse RFC 3339 Date
    '''
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

class FeedException(Exception):
    pass

class AtomFeed:
    def __init__(self, _url):
        self.url = _url
        xml = self._get_feed()
        entries = self._parse(xml)
        self.entries = entries
        pass

    def _get_feed(self):
        resp = requests.get(self.url)
        if resp.status_code >= 400:
            raise FeedException(f'Failed to get Feed: {resp.status_code}')

        return resp.content

    def get_latest(self, _exclude: list[str] = [], _include: list[str] = []):
        '''
        _include is ignored if empty. NOT REGEX!!
        '''
        latest ={ }

        for entry in self.entries:
            if len(latest) <= 0  or date_compare(entry['updated'], latest['updated']):
                if containts_any_of(entry['title'], _exclude):
                    continue
                if not (len(_include) == 0 or containts_any_of(entry['title'], _include)):
                    continue

                latest = entry

        return latest


    def _parse(self, xml):
        tree = ET.fromstring(xml)

        entries = []

        for entry in tree:
            if not entry.tag.endswith('entry'):
                continue

            data = {}

            for att in entry:
                if att.tag.endswith('updated'):
                    data['updated'] = att.text

                if att.tag.endswith('title'):
                    data['title'] = att.text

                if att.tag.endswith('link'):
                    data['link'] = att.attrib['href']

            entries.append(data)

        return entries
