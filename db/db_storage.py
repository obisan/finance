import psycopg2


class StorageDb:

    def __init__(self, host, port, dbname, user, password):
        self.connection = \
            psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password)

    def get_data(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM cot_report_type LIMIT 10')
        records = cursor.fetchall()
        cursor.close()
        self.connection.close()
        return records
