import json


class ConfigurationReader:
    @staticmethod
    def read_config():
        with open('config.json') as json_file:
            json_data = json.load(json_file)
            return json_data
