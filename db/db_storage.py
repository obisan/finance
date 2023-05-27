import configparser

import psycopg2
from psycopg2 import sql


class StorageDb:

    def __init__(self, host=None, port=None, dbname=None, user=None, password=None, filename=None):
        if filename:
            self._init_from_file(filename)
        else:
            self._init_from_params(host, port, dbname, user, password)

    def _init_from_file(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)

        host = config['DEFAULT']['host']
        port = config['DEFAULT']['port']
        dbname = config['DEFAULT']['dbname']
        user = config['DEFAULT']['user']
        password = config['DEFAULT']['password']

        self._init_from_params(host, port, dbname, user, password)

    def _init_from_params(self, host, port, dbname, user, password):
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password)
        self.connection.set_session(autocommit=True)

    def get_cot_report_type(self):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM cot_report_type')
            records = cursor.fetchall()
        return records

    def get_setting(self, param_name):
        with self.connection.cursor() as cursor:
            select = "SELECT trim(param_value) FROM setting WHERE param_name = %s"
            cursor.execute(select, (param_name,))
            records = cursor.fetchone()
        return records[0]

    def get_dailybulletin_reports(self):
        with self.connection.cursor() as cursor:
            select = "SELECT trim(name), trim(path) FROM dailybulletin_reports"
            cursor.execute(select, )
            records = cursor.fetchall()
        return records

    def get_dailybulletin_reports_by_names(self, names):
        with self.connection.cursor() as cursor:
            select = "SELECT id, trim(name) FROM dailybulletin_reports WHERE name IN %s"
            cursor.execute(select, (tuple(names),))
            records = cursor.fetchall()
        return records

    def get_dailybulletin_sections_by_id(self, id):
        with self.connection.cursor() as cursor:
            select = "SELECT id, trim(name) FROM dailybulletin_sections WHERE id IN %s"
            cursor.execute(select, (tuple(id),))
            records = cursor.fetchall()
        return records

    def insert_dailybulletin_reports(self, name, date, index, path):
        with self.connection.cursor() as cursor:
            values = [(name, date, index, path)]
            insert = \
                sql.SQL('INSERT INTO dailybulletin_reports (name, date, index, path) VALUES {}'). \
                    format(sql.SQL(',').join(map(sql.Literal, values)))
            cursor.execute(insert)
