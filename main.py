import logging
import sys
from time import sleep

from configuration_reader import ConfigurationReader
from domoticz_connector import DomoticzConnector
from yeelight_connector import YeelightConnector

_logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger = logging.root
    logger.setLevel('INFO')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setStream(sys.stdout)
    logger.addHandler(ch)


    _logger.info("Starting agent")
    configuration = ConfigurationReader.read_config()
    domoticz_url = configuration['domoticz_url']
    domoticz_user = configuration['domoticz_user']
    domoticz_pass = configuration['domoticz_pass']
    _logger.info("Domoticz URL {}".format(domoticz_url))

    devices = configuration['devices']

    timeout_secs = configuration['timeout_secs']
    _logger.info("Timeout sleep secs - {}".format(timeout_secs))

    domoticz_connector = DomoticzConnector(domoticz_url, domoticz_user, domoticz_pass)

    while True:
        sleep(timeout_secs)
        for device in devices:
            try:
                domoticz_id = device['domoticz_id']
                device_ip = device['device_ip']
                yeelight_connector = YeelightConnector(device_ip)
                domoticz_status = domoticz_connector.get_switch_status(domoticz_id)
                real_status = yeelight_connector.get_status()
                if domoticz_status != real_status:
                    _logger.info('Device {}:{} - update status to {}'.format(domoticz_id, device_ip, domoticz_status))
                    yeelight_connector.set_status(domoticz_status)
            except Exception as exp:
                _logger.error(exp)
