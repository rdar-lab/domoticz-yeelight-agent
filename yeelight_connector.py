from yeelight import Bulb


class YeelightConnector:
    def __init__(self, bulb_ip):
        self._bulb_ip = bulb_ip
        self._bulb = Bulb(self._bulb_ip)

    def get_status(self):
        props = self._bulb.get_properties()
        if props is None:
            raise Exception('Invalid state, prop is None')

        if 'power' not in props:
            raise Exception('Invalid state, props not valid - {}'.format(props))

        return props['power'].lower() == 'on'

    def set_status(self, status):
        if status:
            self._bulb.turn_on()
        else:
            self._bulb.turn_off()

