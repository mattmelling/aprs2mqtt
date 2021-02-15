import os
import unittest
from .config import Config

class TestConfig(unittest.TestCase):
    def test_get_config(self):
        config = Config({
            'aprs': {
                'host': 'localhost'
            }
        })
        self.assertEqual(config.get_config('aprs', 'host'), 'localhost')
    def test_get_config_env(self):
        config = Config({})
        os.environ['APRS_HOST'] = 'localhost'
        self.assertEqual(config.get_config('aprs', 'host'), 'localhost')
