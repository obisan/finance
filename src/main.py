import sys

from bs4 import BeautifulSoup

from db.db_storage import StorageDb
from scenario.dailybulletinsync import DailybulletinSync

if __name__ == '__main__':
    # sys.argv[0] path.py
    # sys.argv[1] --config
    # sys.argv[2] config.xml

    with open(sys.argv[2], 'r') as file:
        xml_data = file.read()
        soup = BeautifulSoup(xml_data, "xml")
        credentials_filename = soup.find("config").find("connect").text

    storageDb = StorageDb(filename=credentials_filename)

    dailybulletinSync = DailybulletinSync(storageDb)
    dailybulletinSync.sync_exec()

    # ============================================================================
    # connection = mysql_helper()
    # for user_report in connection.get_user_reports():
    #     setting = connection.get_setting(user_report['report_id'])
    #     user_report_axis = connection.get_user_report_axis(user_report['user_report_id'])
    #     user_report_commodity = connection.get_user_report_commodity(user_report['user_report_id'])
    #     futures = futures(user_report, user_report_commodity, user_report_axis, setting, 2019)
    #     code = futures.run()

    sys.exit(0)
