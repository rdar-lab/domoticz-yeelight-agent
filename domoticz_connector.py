import requests
import json


class DomoticzConnector:
    def __init__(self, url, user, password):
        self._url = url
        self._user = user
        self._password = password

    def _perform_request(self, command):
        r = requests.get(self._url + command, auth=(self._user, self._password), verify=False)
        if r.status_code == 200:
            j = json.loads(r.text)
            return j
        else:
            raise Exception('HTTP Error : ' + str(r.status_code) + ' - ' + r.text)

    def get_switch_status(self, switch_id):
        call_result = self._perform_request('/json.htm?type=devices&rid={}'.format(switch_id))
        if 'result' not in call_result:
            raise Exception("Result was not valid - {}".format(call_result))

        if len(call_result['result']) != 1:
            raise Exception("Result count not valid - {}".format(call_result))

        result_item = call_result['result'][0]
        if 'idx' not in result_item or result_item['idx'] != switch_id:
            raise Exception("Result IDX is not as expected - {}".format(call_result))

        if 'Status' not in result_item:
            raise Exception("Result item does not have status - {}".format(call_result))

        return result_item['Status'].lower() == 'on'
