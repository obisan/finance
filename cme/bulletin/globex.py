import bisect


class Globex:
    def __init__(self, storage_db=None):
        self.storage_db = storage_db

        self.contracts_symbol_month = self.storage_db.get_dailybulletin_contracts_symbol_month()
        self.contracts_symbol_month.sort(key=lambda x: x[1])
        self.contracts_symbol_month_values = [symbol_month[1] for symbol_month in self.contracts_symbol_month]

    def convert(self, month, year, product):
        index = bisect.bisect_left(self.contracts_symbol_month_values, month)
        if index != len(self.contracts_symbol_month) and self.contracts_symbol_month[index][1] == month:
            return product + self.contracts_symbol_month[index][0] + year[3]
