import os
import logging
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class Config:
    @staticmethod
    def from_file(filename, logger=None):
        logger.info(f'Config.from_file({filename})')
        with open(filename, 'r') as f:
            return Config(yaml.load(f, Loader=Loader), logger)

    def __init__(self, config, logger=None):
        self._config = config
        self._logger = logger if logger is not None else logging.getLogger()

    def get_config(self, section, name):
        self._logger.debug(f'Config.get_config {section}.{name}')
        if section in self._config and name in self._config[section]:
            return self._config[section][name]
        env = f'{section.upper()}_{name.upper()}'
        if env in os.environ:
            return os.environ[env]
        return None

    def get_aprs_host(self):
        return self.get_config('aprs', 'host')

    def get_aprs_port(self):
        return self.get_config('aprs', 'port')

    def get_aprs_login(self):
        return self.get_config('aprs', 'login')

    def get_mqtt_host(self):
        return self.get_config('mqtt', 'host')

    def get_mqtt_port(self):
        return self.get_config('mqtt', 'port')

    def get_mqtt_user(self):
        return self.get_config('mqtt', 'user')

    def get_mqtt_pass(self):
        return self.get_config('mqtt', 'pass')

    def get_consumers(self):
        self._logger.debug('Config.get_consumers')
        if 'consumers' in self._config:
            return self._config['consumers']
        return []
