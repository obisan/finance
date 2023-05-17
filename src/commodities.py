import json
import os


class cl_commodities:
    __instance = None

    data = None

    @staticmethod
    def get_instance():
        if cl_commodities.__instance is None:
            cl_commodities.__instance = cl_commodities()
        return cl_commodities.__instance

    def __init__(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'z_trd_commodities.json')
        with open(filename) as json_file:
            self.data = json.load(json_file)
