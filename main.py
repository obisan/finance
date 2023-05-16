import sys

from db.db_storage import StorageDb
from scenario.dailybulletinsync import DailybulletinSync

if __name__ == '__main__':
    # fd = open('config.xml', 'r')
    # xml_file = fd.read()
    # soup = BeautifulSoup(xml_file, 'lxml')
    # for tag in soup.findAll("item"):
    #     print(tag)
    #     print(tag["name"])
    #     print(tag.text)
    # fd.close()

    storageDb = StorageDb(filename='connect.ini')

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
