import bisect

import pandas as pd
import requests

from constants import Setting


class CmeProductSync:
    def __init__(self, storage_db, logger=None):
        self.storage_db = storage_db
        self.logger = logger

        self.skip_rows = 1
        self.product_url = self.storage_db.get_setting(Setting.CME_PRODUCT_URL.value)
        self.columns_to_parse = ['CME Group Product Name', 'Futures/Options', 'Globex', 'Clearport']

    def sync_exec(self):
        with requests.get(self.product_url) as response:
            if response.status_code == 200:
                xlsx_content = response.content

                # Parse the XLSX file and extract the specified columns
                df = pd.read_excel(xlsx_content, sheet_name="FX", skiprows=self.skip_rows)
                df.columns = df.columns.str.strip()

                # Print the parsed data
                parsed_data = df[self.columns_to_parse]
                product_names = df['CME Group Product Name'].values.tolist()

                products = self.storage_db.get_dailybulletin_products(product_names)
                products.sort(key=lambda product: product[0])

                products_insert = []
                products_update = []
                for index, row in parsed_data.iterrows():
                    product_name = row['CME Group Product Name']
                    product_type = row['Futures/Options']
                    globex = row['Globex']
                    clearport = row['Clearport']

                    # index = bisect.bisect_left(products, product_name)
                    index = bisect.bisect_left([product[0] for product in products], product_name)
                    if index != len(products) and products[index][0] == product_name:
                        if products[index][1] != product_type \
                                or products[index][2] != globex \
                                or products[index][3] != clearport:
                            products_update.append(
                                {
                                    'product_name': product_name,
                                    'type': product_type,
                                    'globex': globex,
                                    'clearport': clearport
                                }
                            )
                    else:
                        products_insert.append(
                            {
                                'product_name': product_name,
                                'type': product_type,
                                'globex': globex,
                                'clearport': clearport
                            }
                        )
                        self.logger.info()

                if len(products_insert) != 0:
                    self.storage_db.insert_dailybulletin_products(products_insert)
                if len(products_update) != 0:
                    self.storage_db.update_dailybulletin_products(products_update)
