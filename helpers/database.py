import pymysql
from pymysql.cursors import DictCursor


class mysql_helper:

    def __init__(self):
        self.connection = pymysql.connect(
            host='192.168.88.100',
            user='finance',
            password='c3NI5orEguhOT7HOq34AB5YOt567H1',
            db='finance',
            charset='utf8mb4',
            cursorclass=DictCursor)

    def __del__(self):
        self.connection.close()

    def cursor(self):
        return self.connection.cursor()

    def get_cot_reports(self):
        s = []
        query = 'select * from cot_reports'

        with self.cursor() as cursor:
            cursor.execute(query)

        for row in cursor:
            s.append(row)

        return s

    def get_cot_attributes(self):
        s = []
        query = 'select * from cot_attributes'

        with self.cursor() as cursor:
            cursor.execute(query)

        for row in cursor:
            s.append(row)

        return s

    def get_cot_commodities(self):
        s = []
        query = 'select * from cot_commodities'

        with self.cursor() as cursor:
            cursor.execute(query)

        for row in cursor:
            s.append(row)

        return s

    def get_cot_reports(self):
        s = []
        query = 'select * from cot_reports'

        with self.cursor() as cursor:
            cursor.execute(query)

        for row in cursor:
            s.append(row)

        return s

    def get_cot_attributes(self):
        s = []
        query = 'select * from cot_attributes'

        with self.cursor() as cursor:
            cursor.execute(query)

        for row in cursor:
            s.append(row)

        return s

    def get_cot_report_commodities(self):
        s = []
        query = '' \
                'select ' \
                'report_id,' \
                'commodity_id,' \
                'r.name as report_name,' \
                'd.name as commodity_name ' \
                'from cot_report_commodities    as c' \
                'inner join cot_reports         as r on r.id = report_id ' \
                'inner join cot_commodities     as d on d.id = commodity_id '

        with self.cursor() as cursor:
            cursor.execute(query)

        for row in cursor:
            s.append(row)

        return s

    def get_setting(self, report_id):
        s = []
        query = '' \
                'select * ' \
                'from settings ' \
                'join cot_reports as c on c.id = report_id ' \
                'where c.id=(%s)'
        with self.cursor() as cursor:
            cursor.execute(query, (report_id,))

        for row in cursor:
            s.append(row)

        return s[0]

    def get_settings(self):
        s = []
        query = '' \
                'select * ' \
                'from settings '

        with self.cursor() as cursor:
            cursor.execute(query)

        for row in cursor:
            s.append(row)

        return s

    def get_user_report(self, user_report_id):
        s = []
        query = '' \
                'SELECT ' \
                'c.id as user_report_id, ' \
                'c.report_id, ' \
                'c.commodity_id, ' \
                'd.name as name_commodity, ' \
                'a.axis, ' \
                'a.`key`, ' \
                'a.hide, ' \
                'a.attribute_id, ' \
                'b.name as name_axis ' \
                'FROM user_report		AS c ' \
                'JOIN user_report_axis  AS a ON a.user_report_id 	= c.id ' \
                'JOIN cot_attributes 	AS b ON b.id 				= a.attribute_id ' \
                'JOIN cot_commodities   AS d ON d.id 				= c.commodity_id ' \
                'where c.id=(%s)'

        with self.cursor() as cursor:
            cursor.execute(query, user_report_id)

        for row in cursor:
            s.append(row)

        return s

    def get_user_report_axis(self, user_report_id):
        s = []
        query = '' \
                'SELECT ' \
                'a.id AS user_report_id, ' \
                'b.attribute_id, ' \
                'c.name, ' \
                'b.axis, ' \
                'b.`key`, ' \
                'b.hide ' \
                'FROM user_report AS a ' \
                'JOIN user_report_axis AS b ON b.user_report_id = a.id ' \
                'JOIN cot_attributes AS c ON c.id = b.attribute_id ' \
                'where user_report_id=(%s) '

        with self.cursor() as cursor:
            cursor.execute(query, user_report_id)

        for row in cursor:
            s.append(row)

        return s

    def get_user_reports(self):
        s = []
        query = '' \
                'SELECT ' \
                'a.id as user_report_id, ' \
                'a.name as user_report_name, ' \
                'b.id AS report_id, ' \
                'b.name as report_name, ' \
                'c.id AS commodity_id, ' \
                'c.name as commodity_name ' \
                'FROM user_report AS a ' \
                'JOIN cot_reports AS b ON a.report_id 		= b.id ' \
                'JOIN cot_commodities AS c ON a.commodity_id	= c.id '

        with self.cursor() as cursor:
            cursor.execute(query)

        for row in cursor:
            s.append(row)

        return s

    def get_user_report_commodity(self, user_report_id):
        values = self.get_user_report(user_report_id)

        result = []

        for line in values:
            if line['name_commodity'] not in [x['name_commodity'] for x in result]:
                result.append({'id': line['commodity_id'], 'name_commodity': line['name_commodity']})

        return result
