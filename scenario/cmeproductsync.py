import pandas as pd
import requests

from constants import Setting


class CmeProductSync:
    def __init__(self, storage_db, logger=None):
        self.storage_db = storage_db
        self.logger = logger

        self.product_url = self.storage_db.get_setting(Setting.CME_PRODUCT_URL.value)
        self.columns_to_parse = ['CME Group Product Name', 'Futures/Options', 'Globex', 'Clearport']

    def sync_exec(self):
        with requests.get(self.product_url) as response:
            if response.status_code == 200:
                xlsx_content = response.content

                # Parse the XLSX file and extract the specified columns
                skip_rows = 1

                df = pd.read_excel(xlsx_content, sheet_name="FX", skiprows=skip_rows)
                df.columns = df.columns.str.strip()

                parsed_data = df[self.columns_to_parse]

                # Print the parsed data
                s = parsed_data['CME Group Product Name'].values.tolist()

                sss = self.storage_db.get_dailybulletin_products()

                print(sss)
