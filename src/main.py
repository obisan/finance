import sys

from bs4 import BeautifulSoup

from constants.enums import ModeExecution
from db.db_storage import StorageDb
from log.Logger import Logger
from scenario.cmeproductsync import CmeProductSync
from scenario.dailybulletinanalysis import DailyBulletinAnalysis
from scenario.dailybulletinsync import DailybulletinSync

if __name__ == '__main__':
    # sys.argv[0] path.py
    # sys.argv[1] --config
    # sys.argv[2] config.xml

    try:

        with open(sys.argv[2], 'r') as file:
            xml_data = file.read()
            soup = BeautifulSoup(xml_data, "xml")
            credentials_filename = soup.find("config").find("connect").text
            mode = soup.find("config").find("mode").text

            match mode:
                case ModeExecution.DAILYBULLETIN_SYNC.value:
                    storageDb = StorageDb(filename=credentials_filename)

                    dailybulletinSync = DailybulletinSync(storageDb, Logger())
                    dailybulletinSync.sync()
                case ModeExecution.DAILYBULLETIN_ANALYSIS.value:
                    storageDb = StorageDb(filename=credentials_filename)

                    dailybulletinAnalysis = DailyBulletinAnalysis(storageDb, Logger())
                    dailybulletinAnalysis.analysis()
                case ModeExecution.DAILYBULLETIN_SYNC_PRODUCTS.value:
                    storageDb = StorageDb(filename=credentials_filename)

                    cmeProductSync = CmeProductSync(storageDb, Logger())
                    cmeProductSync.sync()

    except Exception as e:
        Logger().critical(e)

    # ============================================================================
    # connection = mysql_helper()
    # for user_report in connection.get_user_reports():
    #     setting = connection.get_setting(user_report['report_id'])
    #     user_report_axis = connection.get_user_report_axis(user_report['user_report_id'])
    #     user_report_commodity = connection.get_user_report_commodity(user_report['user_report_id'])
    #     futures = futures(user_report, user_report_commodity, user_report_axis, setting, 2019)
    #     code = futures.run()

    sys.exit(0)
