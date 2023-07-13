import io

import pandas as pd
import requests

from constants import Setting


class DailyBulletinSyncContract:
    def __init__(self, storage_db, logger=None):
        self.storage_db = storage_db
        self.logger = logger

        self.columns = [
            'Option First Avail Date',
            'Option Expiration Date (CT)',
            'Option Product',
            'Option Symbol',
            'Underlying Symbol',
            'Underlying Expiration Date (CT)']

        self.skip_rows = 0
        self.contract_url = self.storage_db.get_setting(Setting.CME_CONTRACT_URL.value)
        self.products_url = [
            self.storage_db.get_setting(Setting.CME_PRODUCT_URL_EUR.value),
            self.storage_db.get_setting(Setting.CME_PRODUCT_URL_AUD.value),
            self.storage_db.get_setting(Setting.CME_PRODUCT_URL_JPY.value),
            self.storage_db.get_setting(Setting.CME_PRODUCT_URL_GBP.value),
            self.storage_db.get_setting(Setting.CME_PRODUCT_URL_CHF.value),
            self.storage_db.get_setting(Setting.CME_PRODUCT_URL_CAD.value)]

    def sync(self):
        for product_url in self.products_url:
            with requests.get(product_url) as response:
                if response.status_code == 200:
                    csv_content = response.content
                    csv_file = io.BytesIO(csv_content)

                    df = pd.read_csv(csv_file, skiprows=self.skip_rows)
                    df.columns = df.columns.str.strip()

                    parsed_data = df[self.columns]

                    print(parsed_data.head())



        self.storage_db.insert_dailybulletin_contracts()

    def exec_sync(self):
        s = 0
