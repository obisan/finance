import pandas as pd

from helpers.database import mysql_helper
from helpers.downloader_cot import Downloader_cot
from utils import cl_utils


class Loader:

    def __init__(self, user_report, user_report_commodity, user_report_axis, settings, target_year):
        self.settings = settings
        self.target_year = target_year
        self.user_report = user_report
        self.user_report_commodity = user_report_commodity
        self.user_report_axis = user_report_axis
        self.path_data = settings['path'] + settings['scr_file'] + str(target_year) + '.' + settings['extension1']

    def run(self):
        downloader = Downloader_cot(self.settings, self.target_year)

        if downloader.download_by_year() != 0:
            return 1

        return 0

    def get_data(self):
        data = cl_utils.get_data_by_commodities(
            self.path_data,
            self.user_report_commodity,
            self.user_report_axis)

        return data

    def save2db(self):
        connection = mysql_helper()
        commodities = connection.get_cot_commodities()
        print(commodities)

        df = pd.read_csv(self.path_data)

        # for line in df.values:
        #    print(line)

        return 0
