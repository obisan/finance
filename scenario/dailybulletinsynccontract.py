import bisect
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
        expirations = []
        total = []
        for product_url in self.products_url:
            with requests.get(product_url) as response:
                if response.status_code == 200:
                    csv_content = response.content
                    csv_file = io.BytesIO(csv_content)

                    df = pd.read_csv(csv_file, skiprows=self.skip_rows)
                    df.columns = df.columns.str.strip()

                    parsed_data = df[self.columns]
                    total.append(parsed_data)  # Append parsed_data to the total list

        # Concatenate all parsed data into a single DataFrame
        combined_data = pd.concat(total)

        unique_products = combined_data['Option Product'].unique()
        products = self.storage_db.get_dailybulletin_products_by_names(unique_products)

        products.sort(key=lambda x: x[1])
        products_values = [product[1] for product in products]

        for index, row in combined_data.iterrows():
            option_symbol = row['Option Symbol']
            option_product = row['Option Product']
            underlying_symbol = row['Underlying Symbol']
            option_avail_date = row['Option First Avail Date']
            option_expiration_date = row['Option Expiration Date (CT)']
            underlying_expiration_date = row['Underlying Expiration Date (CT)']

            index_product = bisect.bisect_left(products_values, option_product)
            if index_product != len(products) and products[index_product][1] == option_product:
                product_id = products[index_product][0]
            else:
                continue

            expirations.append({
                'option_symbol': option_symbol,
                'product_id': product_id,
                'underlying_symbol': underlying_symbol,
                'option_first_avail_date': option_avail_date,
                'option_expiration_date': option_expiration_date,
                'underlying_expiration_date': underlying_expiration_date})

        if len(expirations) != 0:
            self.storage_db.insert_dailybulletin_expiration(expirations)

    def exec_sync(self):
        s = 0
