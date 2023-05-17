import json
import os


class cl_settings:
    __instance = None

    data = None

    @staticmethod
    def get_instance():
        if cl_settings.__instance is None:
            cl_settings.__instance = cl_settings()
        return cl_settings.__instance

    def __init__(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'z_trd_settings.json')
        with open(filename) as json_file:
            self.data = json.load(json_file)
