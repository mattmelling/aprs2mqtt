import json
import unittest
from unittest.mock import patch, Mock, MagicMock, DEFAULT
from .config import Config

class TestAprs(unittest.TestCase):

    @patch('paho.mqtt.publish.single')
    def test_handler(self, mock_publish):
        from .aprs2mqtt import Aprs2MqttService
        mock_publish = MagicMock()
        config = Config({
            'mqtt': {
                'host': 'localhost',
                'port': 1883,
                'user': 'user',
                'pass': 'pass'
            }
        })
        svc = Aprs2MqttService(config)
        svc.handler({ 'topic': 'topic' },
                    { 'message': 'ok' })
        mock_publish.asset_called_with(
            'topic',
            payload=json.dumps({ 'message': 'ok' }),
            hostname='localhost',
            port=1883,
            client_id='user',
            auth={
                'username': 'user',
                'password': 'pass'
            }
        )

    @patch('aprslib.IS')
    def test_run(self, mock_is):
        from .aprs2mqtt import Aprs2MqttService
        config = Config({
            'aprs': {
                'host': 'localhost',
                'port': 1,
                'login': 'test'
            },
            'consumers': [
                { 'filter': 'filter', 'topic': 'topic' }
            ]
        })
        svc = Aprs2MqttService(config)
        svc.run()
        mock_is.assert_called_with('test', host='localhost', port=1)

    @patch.multiple('aprslib.IS', connect=DEFAULT,
                    set_filter=DEFAULT, consumer=DEFAULT)
    def test_connect(self, connect, set_filter, consumer):
        from .aprs2mqtt import Aprs2MqttService
        config = Config({
            'aprs': {
                'host': 'localhost',
                'port': 1,
                'login': 'test'
            },
            'consumers': [
                { 'filter': 'filter', 'topic': 'topic' }
            ]
        })
        svc = Aprs2MqttService(config)
        svc.run()
        connect.assert_called()
        set_filter.assert_called_with('filter')
        consumer.assert_called()
