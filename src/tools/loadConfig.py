from configparser import ConfigParser
from os import path
from typing import List

class ErrorSetConfigFailed(Exception):
    def __init__(self, error):
        super().__init__(error)


class ConfigLoader:
    def __init__(self, pth: str = None):
        if pth:
            self.path = pth
        else:
            self.path = path.join('.', 'component', 'app.cfg')

        self.config = ConfigParser()
        self.config.read(self.path)

    def getConfig(self):
        return self.config

    def getConfigSection(self, section):
        return self.config[section]

    def getConfigOption(self, section, option):
        return self.config[section][option]

    def setConfigOption(self, section, option, value):
        self.config[section][option] = value
        try:
            with open(self.path, 'w') as configfile:
                self.config.write(configfile)

        finally:
            return value, section, option



    @staticmethod
    def yn2bool(value: str) -> bool:
        if value.lower() == 'enable':
            return True
        elif value.lower() == 'disable':
            return False
        else:
            raise ValueError('Invalid input', value)

    @staticmethod
    def bool2yn(value: bool) -> str:
        if value:
            return 'Enable'
        else:
            return 'Disable'

    @staticmethod
    def str2intarr(value: str) -> List[int]:
        return [int(x) for x in value.split(',')]

    @staticmethod
    def intarr2str(value: List[int]) -> str:
        return ', '.join(str(x) for x in value)

    @staticmethod
    def str2strarr(value: str):
        return value.replace(' ','').split(',')

    @staticmethod
    def strarr2str(value: List[str]):
        return ', '.join(value)
