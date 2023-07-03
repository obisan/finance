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


class Globex:
    def __init__(self, storage_db):
        self.storage_db = storage_db
        self.contracts_symbol_month = self.storage_db.get_dailybulletin_report_contracts_symbol_month()
        self.globex_symbol = []

    def build(self, product_globex):
        for globex in product_globex:
            for symbol in self.contracts_symbol_month:
                for i in range(0, 10):
                    self.globex_symbol.append(
                        str(globex) + str(symbol[0]) + str(i))

    def clear(self):
        self.globex_symbol = []

    def get_globex_list(self, product_globex):
        self.clear()
        self.build(product_globex)
        return self.globex_symbol

    def convert_globex_to_list(self, globex):
        self.clear()
        self.build([globex])
        return self.globex_symbol


class DailyBulletinSyncProduct:
    def __init__(self, storage_db, logger=None):
        self.storage_db = storage_db
        self.logger = logger

        self.globex = Globex(storage_db)

        self.skip_rows = 1
        self.product_url = self.storage_db.get_setting(Setting.CME_PRODUCT_URL.value)
        self.columns_to_parse = \
            [ProductColumns.PRODUCT_NAME.value,
             ProductColumns.FUTURES_OPTIONS.value,
             ProductColumns.GLOBEX.value,
             ProductColumns.CLEARPORT.value]

        self.contracts_symbol_month = self.storage_db.get_dailybulletin_report_contracts_symbol_month()

        self.unique_globex_insert, self.unique_globex_symbol_insert = [], []
        self.product_symbols = []
        self.products_insert, self.products_update = [], []

    def sync(self):
        with requests.get(self.product_url) as response:
            if response.status_code == 200:
                xlsx_content = response.content

                # Parse the XLSX file and extract the specified columns
                df = pd.read_excel(xlsx_content, sheet_name="FX", skiprows=self.skip_rows)
                df.columns = df.columns.str.strip()

                self.prepare_unique_globex(df)
                self.prepare_unique_symbol_globex(df)
                self.prepare_product(df)
                self.prepare_product_symbols(df)
                self.sync_exec()

    def prepare_unique_globex(self, df):
        product_globex = df[ProductColumns.GLOBEX.value].unique().tolist()

        unique_globexes = self.storage_db.get_unique_globex()
        unique_globexes.sort(key=lambda l_globex: l_globex[0])

        for globex in product_globex:
            index = bisect.bisect_left([unique_globex[0] for unique_globex in unique_globexes], globex)

            if index != len(unique_globexes) and unique_globexes[index][0] == globex:
                continue

            self.unique_globex_insert.append(globex)
            self.logger.info(f"Saved globex {globex}")

    def prepare_unique_symbol_globex(self, df):
        product_globex = df[ProductColumns.GLOBEX.value].unique().tolist()

        unique_globex_symbols = self.storage_db.get_unique_globex_symbol()
        unique_globex_symbols.sort(key=lambda l_globex: l_globex[0])

        unique_globex_symbol_values = [unique_globex_symbol[0] for unique_globex_symbol in unique_globex_symbols]

        globex_list = self.globex.get_globex_list(product_globex)
        self.globex.clear()

        for globex in globex_list:
            index = bisect.bisect_left(unique_globex_symbol_values, globex)

            if index != len(unique_globex_symbols) and unique_globex_symbols[index][0] == globex:
                continue

            self.unique_globex_symbol_insert.append(
                {
                    'globex_symbol': globex
                }
            )
            self.logger.info(f"Saved globex_symbol {globex}")

    def prepare_product(self, df):
        parsed_data = df[self.columns_to_parse]
        product_names = df[ProductColumns.PRODUCT_NAME.value].values.tolist()

        products = self.storage_db.get_dailybulletin_products_by_names(product_names)
        products.sort(key=lambda product: product[1])
        products_values = [product[1] for product in products]

        for index, row in parsed_data.iterrows():
            name = row[ProductColumns.PRODUCT_NAME.value]
            type = row[ProductColumns.FUTURES_OPTIONS.value]
            globex = row[ProductColumns.GLOBEX.value]
            clearport = row[ProductColumns.CLEARPORT.value]

            index = bisect.bisect_left(products_values, name)
            if index != len(products) and products[index][1] == name:
                if products[index][2] != type \
                        or products[index][3] != globex \
                        or products[index][4] != clearport:
                    self.products_update.append(
                        {
                            'name': name,
                            'type': type,
                            'globex': globex,
                            'clearport': clearport
                        }
                    )
            else:
                self.products_insert.append(
                    {
                        'name': name,
                        'type': type,
                        'globex': globex,
                        'clearport': clearport
                    }
                )
                self.logger.info(f"Saved product {name} {type} {globex} {clearport}")

    def prepare_product_symbols(self, df):
        parsed_data = df[self.columns_to_parse]
        product_names = df[ProductColumns.PRODUCT_NAME.value].values.tolist()

        products = self.storage_db.get_dailybulletin_products_by_names(product_names)
        products.sort(key=lambda product: product[1])
        products_values = [product[1] for product in products]

        products_symbols_db = self.storage_db.get_dailybulletin_products_symbol()
        products_symbols_db.sort(key=lambda product_symbol: (product_symbol[1], product_symbol[2]))
        products_symbols_db_values = [(product_symbol[1], product_symbol[2]) for product_symbol in products_symbols_db]

        for index, row in parsed_data.iterrows():
            name = row[ProductColumns.PRODUCT_NAME.value]
            globex = row[ProductColumns.GLOBEX.value]

            list_globex = self.globex.convert_globex_to_list(globex)

            for current_globex in list_globex:

                left = bisect.bisect_left(products_symbols_db_values, (name, current_globex))
                right = bisect.bisect_right(products_symbols_db_values, (name, current_globex))

                current_product = products_symbols_db[left:right]

                if len(current_product) != 0:
                    continue

                index = bisect.bisect_left(products_values, name)
                if index != len(products) and products[index][1] == name:
                    product_id = products[index][0]
                else:
                    continue

                self.product_symbols.append(
                    {
                        'product_id': product_id,
                        'symbol_globex': current_globex,
                    }
                )
                self.logger.info(f"Saved product-globex link: {product_id} {current_globex}")

    def sync_exec(self):
        if len(self.unique_globex_insert) != 0:
            self.storage_db.insert_unique_globex(self.unique_globex_insert)
        if len(self.unique_globex_symbol_insert) != 0:
            self.storage_db.insert_unique_globex_symbol(self.unique_globex_symbol_insert)
        if len(self.products_insert) != 0:
            self.storage_db.insert_dailybulletin_products(self.products_insert)
        if len(self.products_update) != 0:
            self.storage_db.update_dailybulletin_products(self.products_update)
        if len(self.product_symbols) != 0:
            self.storage_db.insert_dailybulletin_products_symbol(self.product_symbols)
