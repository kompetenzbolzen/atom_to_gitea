'''
'''


from __future__ import annotations

import typing
import yaml


STRUCTURE={
    'url':str,
    'token':str,
    'owner':str,
    'repo':str,
    'feeds':list,
    'label':str
}

STRUCTURE_DICT_LIST={
        'feeds': {
            'url':str,
            'name':str,
            'assign':str,
            'exclude':list,
            'include':list,
        }
}

DEFAULTS_DICT_LIST={
        'feeds': {
            'url':None,
            'name':None,
            'assign':None,
            'exclude': [],
            'include': []
        }
}



class ConfigError(Exception):
    pass

class Config:
    '''
    Imports and stores curvegenerator parameters

    Example:
        ```yaml
        # test.yaml
        ---
        testval: 4
        ```
        ```python
        conf = Config("test.yaml")
        print(conf.testval)
        ```
    '''
    def __init__(self, _file):
        '''
        Constructor

        Args:
            _file (str): Filename to yaml configfile
        '''

        if _file is None:
            return

        with open(_file, 'r') as f:
            self.config = yaml.load(f.read(), Loader=yaml.FullLoader)

        self._populate_defaults()
        self._validate()

    def __iter__(self):
        self.n = 0
        pass

    def __next__(self):
        pass

    def __getitem__(self, _key):
        self.config[_key]

    @staticmethod
    def _validate_dict(_dict, _spec, _context=''):
        for e in _spec:
            if e not in _dict:
                if _spec[e] is not list:
                    raise ConfigError(f'{_context}Key {e} is not set.')
                else:
                    pass
            elif type(_dict[e]) is not _spec[e]:
                raise ConfigError(f'{_context}Key {e} is {type(_dict[e])}. Should be {_spec[e]}')

    def _populate_defaults(self):
        # this is a holy mess. It works. And at time of writing made sense.
        for lst in DEFAULTS_DICT_LIST:
            for entry in range(len(self.config[lst])):
                for default in DEFAULTS_DICT_LIST[lst]:
                    if not default in self.config[lst][entry]:
                        self.config[lst][entry][default] = DEFAULTS_DICT_LIST[lst][default]

    def _validate(self):
        Config._validate_dict(self.config, STRUCTURE)

        for lst in STRUCTURE_DICT_LIST:
            for e in self.config[lst]:
                Config._validate_dict(e, STRUCTURE_DICT_LIST[lst], 'feeds: ')

    def load(self, _dict):
        self.config = _dict

    def __getattr__(self, _attr) -> str | Config | None:
        if _attr not in self.config:
            return None

        if isinstance(self.config[_attr], dict):
            ret = Config(None)
            ret.load(self.config[_attr])
            return ret

        return self.config[_attr]

    def __str__(self):
        return yaml.dump(self.config)

