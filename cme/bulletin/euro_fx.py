import bisect
import re

from constants.enums import DailyBulletinReportsDataColumns
from constants.enums import DailyBulletinSectionsTypes


class Euro_FX:

    def __init__(self, globex=None):

        self.globex = globex

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
            [DailyBulletinReportsDataColumns.STRIKE.value,
             DailyBulletinReportsDataColumns.OPEN_RANGE.value,
             DailyBulletinReportsDataColumns.HIGH.value,
             DailyBulletinReportsDataColumns.LOW.value,
             DailyBulletinReportsDataColumns.CLOSING_RANGE.value,
             DailyBulletinReportsDataColumns.SETT_PRICE.value,
             DailyBulletinReportsDataColumns.PT_CHGE.value,
             DailyBulletinReportsDataColumns.DELTA.value,
             DailyBulletinReportsDataColumns.EXERCISES.value,
             DailyBulletinReportsDataColumns.VOLUME_TRADES_CLEARED.value,
             DailyBulletinReportsDataColumns.OPEN_INTEREST.value,
             DailyBulletinReportsDataColumns.OPEN_INTEREST_DELTA.value,
             DailyBulletinReportsDataColumns.HIGH.value,
             DailyBulletinReportsDataColumns.LOW.value
             ]

        self.months = [
            {'month': 'APR', 'value': 4},
            {'month': 'AUG', 'value': 8},
            {'month': 'DEC', 'value': 12},
            {'month': 'FEB', 'value': 2},
            {'month': 'JAN', 'value': 1},
            {'month': 'JUL', 'value': 7},
            {'month': 'JUN', 'value': 6},
            {'month': 'MAR', 'value': 3},
            {'month': 'MAY', 'value': 5},
            {'month': 'NOV', 'value': 11},
            {'month': 'OCT', 'value': 10},
            {'month': 'SEP', 'value': 9}]

        self.months.sort(key=lambda x: x['month'])

        self.months_values = [month['month'] for month in self.months]

        self.sections = []
        self.strike_lines = []

    def exec(self, section_content):
        pattern_strike_head = \
            r'(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)(\d{2})\s+(\S{3})\s+OPT'

        contract = ''
        product = ''
        globex = ''
        year = ''
        option_type = DailyBulletinSectionsTypes.PUT.value
        strike_last = {
            'strike': '',
            'strike_index': 0
        }
        for content in section_content:
            matches_option_section = re.match(self.pattern_option_section, content)
            if matches_option_section:
                month = self.convert_month_2_value(contract[0:3])
                year = '20' + str(contract[3:5])
                globex = self.globex.convert(month, year, product)
                self.add_section(globex, year, self.strike_lines)
                self.strike_lines = []
                option_type = DailyBulletinSectionsTypes.CALL.value
                contract = ''
                product = ''

            matches_strike_head = re.match(pattern_strike_head, content)
            if matches_strike_head:
                values = matches_strike_head.groups()
                month = self.convert_month_2_value(values[0])
                year = '20' + str(values[1])
                globex = self.globex.convert(month, year, values[2])
                if (values[0] + values[1]) != contract:
                    self.add_section(globex, year, self.strike_lines)
                    self.strike_lines = []
                    contract = values[0] + values[1]
                    product = ''
                if values[2] != product:
                    self.add_section(globex, year, self.strike_lines)
                    self.strike_lines = []
                    product = values[2]

            matches_columns_data = re.match(self.pattern_contract_data, content)
            if matches_columns_data:
                self.add_strike_line(self.strike_lines, matches_columns_data.groups(), strike_last, option_type)

        return self.sections

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

    def add_section(self, globex, year, strike_lines):
        if len(strike_lines) == 0:
            return
        sections_values = [(section['globex'], section['year']) for section in self.sections]
        index = bisect.bisect_left(sections_values, (globex, year))
        if index != len(self.sections):
            return
        else:
            self.sections.insert(
                index,
                {
                    'globex': globex,
                    'year': year,
                    'strikes': strike_lines
                }
            )

    def add_strike_line(self, strike_lines, values, strike_last, option_type):
        strike_line = dict(zip(self.columns_data, values))

        if strike_line[DailyBulletinReportsDataColumns.STRIKE.value] == strike_last['strike']:
            strike_last['strike_index'] = strike_last['strike_index'] + 1
        else:
            strike_last['strike'] = strike_line[DailyBulletinReportsDataColumns.STRIKE.value]
            strike_last['strike_index'] = 0

        strike_line[DailyBulletinReportsDataColumns.STRIKE_INDEX.value] = strike_last['strike_index']
        strike_line[DailyBulletinReportsDataColumns.TYPE.value] = option_type
        strike_lines.append(strike_line)

    def convert_month_2_value(self, month):
        index = bisect.bisect_left(self.months_values, month)
        if index != len(self.months) and self.months[index]['month'] == month:
            return self.months[index]['value']
