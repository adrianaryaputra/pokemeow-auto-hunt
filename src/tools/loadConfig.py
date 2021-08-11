from configparser import ConfigParser
from os import path

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
    def yn2bool(value):
        if value.lower() == 'enable':
            return True
        elif value.lower() == 'disable':
            return False
        else:
            raise ValueError('Invalid input', value)

    @staticmethod
    def bool2yn(value):
        if value:
            return 'Enable'
        else:
            return 'Disable'
