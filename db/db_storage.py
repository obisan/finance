import configparser

import psycopg2
from psycopg2 import sql

from constants.enums import Setting


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

    def get_cot_report_type(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM cot_report_type')
        records = cursor.fetchall()
        cursor.close()
        self.connection.close()
        return records

    def get_setting(self, param_name):
        cursor = self.connection.cursor()
        select = "SELECT trim(param_value) FROM setting WHERE param_name = %s"

        cursor.execute(select, (param_name,))
        records = cursor.fetchone()
        cursor.close()
        return records[0]

    def get_setting_cme(self):
        records = {
            Setting.CME_FTP_HOST.value: self.get_setting(Setting.CME_FTP_HOST),
            Setting.CME_FTP_USER.value: self.get_setting(Setting.CME_FTP_USER),
            Setting.CME_FTP_PASSWORD.value: self.get_setting(Setting.CME_FTP_PASSWORD)}
        return records

    def insert_dailybulletin_reports(self):
        with self.connection.cursor() as cursor:
            self.connection.autocommit = True
            name = 'sss'
            date = '20120101'
            index = '001'
            path = 'sss/sss'
            values = [
                (name, date, index, path)
            ]
            insert = \
                sql.SQL('INSERT INTO dailybulletin_reports (name, date, index, path) VALUES {}'). \
                    format(sql.SQL(',').join(map(sql.Literal, values)))
            cursor.execute(insert)
