import sys

from constants.enums import ModeExecution
from db.db_storage import StorageDb
from helpers.helpers import Helper
from log.Logger import Logger
from repository import RepositoryBulletin
from scenario.dailybulletinanalysis import DailyBulletinAnalysis
from scenario.dailybulletinsync import DailybulletinSync
from scenario.dailybulletinsynccontract import DailyBulletinSyncContract
from scenario.dailybulletinsyncproduct import DailyBulletinSyncProduct

if __name__ == '__main__':
    # sys.argv[0] path.py
    # sys.argv[1] --config
    # sys.argv[2] config.xml

    try:

        with open(sys.argv[2], 'r') as file:
            xml_path = file.read()
            settings = Helper.get_settings(xml_path)

            filename = settings['filename']
            mode = settings['mode']
            repository = settings['repository']

            match mode:
                case ModeExecution.DAILYBULLETIN_SYNC.value:
                    storageDb = StorageDb(filename=filename)
                    repositoryBulletin = RepositoryBulletin(repository, Logger())

                    dailybulletinSync = DailybulletinSync(storageDb, repositoryBulletin, Logger())
                    dailybulletinSync.sync()
                case ModeExecution.DAILYBULLETIN_ANALYSIS.value:
                    storageDb = StorageDb(filename=filename)
                    repositoryBulletin = RepositoryBulletin(repository, Logger())

                    dailybulletinAnalysis = DailyBulletinAnalysis(storageDb, repositoryBulletin, Logger())
                    dailybulletinAnalysis.analysis()
                case ModeExecution.DAILYBULLETIN_SYNC_PRODUCTS.value:
                    storageDb = StorageDb(filename=filename)

                    cmeProductSync = DailyBulletinSyncProduct(storageDb, Logger())
                    cmeProductSync.sync()
                case ModeExecution.DAILYBULLETIN_SYNC_CONTRACTS.value:
                    storageDb = StorageDb(filename=filename)

                    dailybulletinSyncContract = DailyBulletinSyncContract(storageDb, Logger())
                    dailybulletinSyncContract.sync()

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
