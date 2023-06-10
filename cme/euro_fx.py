import re


class Euro_FX:

    def __init__(self):

        # Контракт это MAR23 | APR23 | MAY23 и т.д.
        self.pattern_contract_head = \
            r'(%s)\s+(\S+)\s+OPT'

        self.pattern_contract_data = \
            r'^(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+\s?[+-]?)\s+(\S+)\s+(\S+)\s+(\S+)\s+(' \
            r'\S+)\s+(\d+\s?[+-]?|-{4})\s+(\S+)\s+(\S+)\s+(\S+)$'

        self.pattern_expiration_name = \
            r'\s+EXPIRATION: ' \
            r'\s+(\w{3}\d{2})' \
            r'\s+(\w{3}\d{2})' \
            r'\s+(\w{3}\d{2})' \
            r'\s+(\w{3}\d{2})' \
            r'\s+(\w{3}\d{2})' \
            r'\s+(\w{3}\d{2})' \
            r'\s+(\w{3}\d{2})' \
            r'\s+(\w{3}\d{2})' \
            r'\s+(\w{3}\d{2})'

        self.pattern_expiration_date = \
            r'\s+EURO FX FUT' \
            r'\s+(\d{2}\/\d{2})' \
            r'\s+(\d{2}\/\d{2})' \
            r'\s+(\d{2}\/\d{2})' \
            r'\s+(\d{2}\/\d{2})' \
            r'\s+(\d{2}\/\d{2})' \
            r'\s+(\d{2}\/\d{2})' \
            r'\s+(\d{2}\/\d{2})' \
            r'\s+(\d{2}\/\d{2})' \
            r'\s+(\d{2}\/\d{2})'

        self.pattern_option_section = \
            r'\s+ADDITIONAL\sEUROFX\s\&\sCME\$INDEX\sCALLS\s\&\sPUTS\s\*\*SETT\.\sPRICE\*\*\s*'

        self.columns_data = \
            ["STRIKE", "OPEN RANGE", "HIGH", "LOW", "CLOSING RANGE", "SETT.PRICE",
             "PT.CHGE.", "DELTA",
             "EXERCISES", "VOLUME TRADES CLEARED", "OPEN INTEREST", "OPEN INTEREST DELTA",
             "HIGH", "LOW"]

    def exec(self, section_content):
        values_expiration = \
            self.expiration(section_content)

        pattern_strike_head = \
            self.pattern_contract_head.replace(
                '%s', ('|'.join([re.escape(name) for name, _, _ in values_expiration])))

        contract = ''
        product = ''
        bulletin = []
        strike_lines = []
        for content in section_content:
            matches_option_section = re.match(self.pattern_option_section, content)
            if matches_option_section:
                contract = ''
                product = ''

            matches_strike_head = re.match(pattern_strike_head, content)
            if matches_strike_head:
                values = matches_strike_head.groups()
                if values[0] != contract:
                    if contract is not None:
                        bulletin.append({'contract': contract, 'product': product, 'strikes': strike_lines})
                    contract = values[0]
                    product = ''
                if values[1] != product:
                    if product is not None:
                        bulletin.append({'contract': contract, 'product': product, 'strikes': strike_lines})
                    product = values[1]

            matches_columns_data = re.match(self.pattern_contract_data, content)
            if matches_columns_data:
                values = matches_columns_data.groups()
                strike_line = dict(zip(self.columns_data, values))
                strike_lines.append(strike_line)

        print(bulletin[0])

    def expiration(self, section_content):
        values_expiration_name, values_expiration_date, values_expiration = (), (), ()

        for content in section_content:
            matches_expiration_name = re.match(self.pattern_expiration_name, content)
            if matches_expiration_name:
                values_expiration_name = matches_expiration_name.groups()

            matches_expiration_date = re.match(self.pattern_expiration_date, content)
            if matches_expiration_date:
                values_expiration_date = matches_expiration_date.groups()

            if values_expiration_name and values_expiration_date:
                break

        if values_expiration_name and values_expiration_date:
            values_expiration = \
                [(name, date, f"20{name[3:5]}.{date.split('/')[0]}.{date.split('/')[1]}")
                 for name, date in zip(values_expiration_name, values_expiration_date)]

        return values_expiration
