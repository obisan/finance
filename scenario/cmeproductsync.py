import bisect
import enum

import pandas as pd
import requests

from constants import Setting


class ProductColumns(enum.Enum):
    PRODUCT_NAME = 'CME Group Product Name'
    FUTURES_OPTIONS = 'Futures/Options'
    GLOBEX = 'Globex'
    CLEARPORT = 'Clearport'


class CmeProductSync:
    def __init__(self, storage_db, logger=None):
        self.storage_db = storage_db
        self.logger = logger

        self.skip_rows = 1
        self.product_url = self.storage_db.get_setting(Setting.CME_PRODUCT_URL.value)
        self.columns_to_parse = \
            [ProductColumns.PRODUCT_NAME.value,
             ProductColumns.FUTURES_OPTIONS.value,
             ProductColumns.GLOBEX.value,
             ProductColumns.CLEARPORT.value]

        self.unique_globex_insert, self.products_insert, self.products_update = [], [], []

    def sync(self):
        with requests.get(self.product_url) as response:
            if response.status_code == 200:
                xlsx_content = response.content

                # Parse the XLSX file and extract the specified columns
                df = pd.read_excel(xlsx_content, sheet_name="FX", skiprows=self.skip_rows)
                df.columns = df.columns.str.strip()

                self.prepare_unique_globex(df)
                self.prepare_product(df)
                self.sync_exec()

    def prepare_unique_globex(self, df):
        product_globex = df[ProductColumns.GLOBEX.value].unique().tolist()

        unique_globexes = self.storage_db.get_unique_globex()
        unique_globexes.sort(key=lambda l_globex: l_globex[0])

        for globex in product_globex:
            index = bisect.bisect_left([unique_globex[0] for unique_globex in unique_globexes], globex)

            if index != len(unique_globexes) and unique_globexes[index][0] == globex:
                continue
            else:
                self.unique_globex_insert.append(globex)
                self.logger.info(f"Saved globex {globex}")

    def prepare_product(self, df):
        parsed_data = df[self.columns_to_parse]
        product_names = df[ProductColumns.PRODUCT_NAME.value].values.tolist()

        products = self.storage_db.get_dailybulletin_products(product_names)
        products.sort(key=lambda product: product[0])

        for index, row in parsed_data.iterrows():
            product_name = row[ProductColumns.PRODUCT_NAME.value]
            product_type = row[ProductColumns.FUTURES_OPTIONS.value]
            globex = row[ProductColumns.GLOBEX.value]
            clearport = row[ProductColumns.CLEARPORT.value]

            index = bisect.bisect_left([product[0] for product in products], product_name)
            if index != len(products) and products[index][0] == product_name:
                if products[index][1] != product_type \
                        or products[index][2] != globex \
                        or products[index][3] != clearport:
                    self.products_update.append(
                        {
                            'product_name': product_name,
                            'type': product_type,
                            'globex': globex,
                            'clearport': clearport
                        }
                    )
            else:
                self.products_insert.append(
                    {
                        'product_name': product_name,
                        'type': product_type,
                        'globex': globex,
                        'clearport': clearport
                    }
                )
                self.logger.info(f"Saved product {product_name} {product_type} {globex} {clearport}")

    def sync_exec(self):
        if len(self.unique_globex_insert) != 0:
            self.storage_db.insert_unique_globex(self.unique_globex_insert)
        if len(self.products_insert) != 0:
            self.storage_db.insert_dailybulletin_products(self.products_insert)
        if len(self.products_update) != 0:
            self.storage_db.update_dailybulletin_products(self.products_update)
