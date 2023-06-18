import io

import pandas as pd
import requests

from constants import Setting


class DailyBulletinSyncContract:
    def __init__(self, storage_db, logger=None):
        self.storage_db = storage_db
        self.logger = logger

        self.skip_rows = 1
        self.contract_url = self.storage_db.get_setting(Setting.CME_CONTRACT_URL.value)
        # self.columns_to_parse = \
        #     [ProductColumns.PRODUCT_NAME.value,
        #      ProductColumns.FUTURES_OPTIONS.value,
        #      ProductColumns.GLOBEX.value,
        #      ProductColumns.CLEARPORT.value]

        # self.unique_globex_insert, self.products_insert, self.products_update = [], [], []

    def sync(self):
        with requests.get(self.contract_url) as response:
            if response.status_code == 200:
                content = response.content
                csv_data = io.StringIO(content.decode('utf-8'))

                df = pd.read_csv(csv_data)
                df.columns = df.columns.str.strip()

                for s in df.values:
                    print(s)

                # pd.set_option('display.max_rows', None)
                # pd.set_option('display.max_columns', None)
                # print(df.head())

        self.storage_db.insert_dailybulletin_contracts()

    def exec_sync(self):
        s = 0
