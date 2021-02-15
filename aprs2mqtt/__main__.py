from .aprs2mqtt import Aprs2MqttService
from .config import Config
import logging
import plac

def _main(config: ("config", "positional")):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('aprs2mqtt')
    cfg = Config.from_file(config, logger)
    Aprs2MqttService.start(cfg, logger=logger)

def main():
    plac.call(_main)

if __name__ == '__main__':
    main()
