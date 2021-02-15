import aprslib
import json
import logging
import signal
import sys
from functools import partial
import paho.mqtt.publish as publish

class Aprs2MqttService:
    @staticmethod
    def start(config, logger=None):
        s = Aprs2MqttService(config,
                             logger=logger)
        s.run()

    def __init__(self, config, logger=None):
        self.logger = (logging.Logger('aprs2mqtt')
                       if logger is None
                       else logger)
        self.config = config
        self.consumers = []
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def handler(self, msg_filter, packet):
        self.logger.debug(f'[{msg_filter}] => {packet}')
        publish.single(msg_filter['topic'],
                       payload=json.dumps(packet),
                       hostname=self.config.get_mqtt_host(),
                       port=int(self.config.get_mqtt_port()),
                       client_id=self.config.get_mqtt_user(),
                       auth={
                           'username': self.config.get_mqtt_user(),
                           'password': self.config.get_mqtt_pass()
                       })

    def run(self):
        login = self.config.get_aprs_login()
        host = self.config.get_aprs_host()
        port = self.config.get_aprs_port()
        for f in self.config.get_consumers():
            rule = f['filter']
            topic = f['topic']
            self.logger.info(f'adding consumer {login}@{host}:{port} - {rule} => {topic}')
            ais = aprslib.IS(login, host=host, port=port)
            ais.connect()
            ais.set_filter(rule)
            ais.consumer(partial(self.handler, f), raw=False)
            self.consumers.append(ais)

    def stop(self, signal, frame):
        self.logger.info(f'Caught signal {signal}, exiting')
        for ais in self.consumers:
            consumer.close()
        sys.exit(0);
