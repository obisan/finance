import bisect
import os
import re
from datetime import datetime

from constants.enums import CME_const
from constants.enums import DailybulletinReportsStatus


def binary_search(bulletins, target):
    names = [bulletin['name'] for bulletin in bulletins]
    index = bisect.bisect_left(names, target)
    if index < len(bulletins) and bulletins[index]['name'] == target:
        return index
    return -1


class DailybulletinSync:

    def __init__(self, storage_db, cme=None, repository=None, logger=None):
        self.storage_db = storage_db
        self.host_save_path = repository.path  # storage_db.get_setting(Setting.HOST_SAVE_PATH.value)
        self.cme = cme
        self.logger = logger

        self.s = []

    def get_dailybulletin_from_cme(self):
        # section/DailyBulletin_pdf_2023021329.zip
        dailybulletin_list = self.cme.get_dailybulletin_list()

        # 0 'section/DailyBulletin_pdf_2023021329'
        # 1 'DailyBulletin_pdf_2023021329'
        # 2 'DailyBulletin_pdf_2023021329.zip'
        # 3 '20230213'
        # 4 '29'
        patterns = [
            r"^(.+)$",
            r"/([^/]+)\.zip$",
            r"/([^/]+)$",
            r"(\d{8})",
            r"\d{8}(\d+)"]

        # transform list values by patterns
        results = [
            [re.search(pattern, filename).group(1) if re.search(pattern, filename) else None
             for pattern in patterns]
            for filename in dailybulletin_list]

        return results

    def get_dailybulletin_from_db(self, bulletins):
        # get records in db by name DailyBulletin_pdf_2023021329, then sort
        dailybulletin_reports_in_db_sorted = \
            sorted(
                [record[1] for record in
                 self.storage_db.get_dailybulletin_reports_by_names(bulletins)],
                key=lambda x: x)
        return dailybulletin_reports_in_db_sorted

    def sync(self):
        self.sync_exec()

    def sync_exec(self):
        dailybulletin_from_cme = self.get_dailybulletin_from_cme()
        # get records in db by name DailyBulletin_pdf_2023021329, then sort
        dailybulletin_from_db = self.get_dailybulletin_from_db(list(map(lambda x: x[1], dailybulletin_from_cme)))

        bulletin_processing = []
        for item in dailybulletin_from_cme:
            target = item[1]
            index = bisect.bisect_left(dailybulletin_from_db, target, )

            if index != len(dailybulletin_from_db) \
                    and dailybulletin_from_db[index] == target:
                self.logger.debug(f"Found: {dailybulletin_from_db[index]}")
                continue

            bulletin_processing.append(
                {
                    'name': item[1],
                    'date': datetime.strptime(item[3], '%Y%m%d').date(),
                    'index': item[4],
                    'path': os.path.join(self.host_save_path, item[2]),
                    'status': DailybulletinReportsStatus.DOWNLOADED.value
                }
            )

        bulletin_downloaded = \
            self.cme.download_dailybulletins_by_name(list(map(lambda x: x['name'], bulletin_processing)))

        for bulletin in bulletin_downloaded:
            self.logger.info(f"Loaded: {bulletin['name']}")

        bulletin_saved = \
            self.save_dailybulletins_downloaded(bulletin_processing, bulletin_downloaded)

        for bulletin in bulletin_saved:
            self.logger.info(f"Saved: {bulletin['name']}")

    def save_dailybulletins_downloaded(self, bulletins, bulletin_downloaded):

        sorted_bulletins = sorted(bulletins, key=lambda x: x['name'])
        bulletins_insert = []
        for downloaded in bulletin_downloaded:
            index = binary_search(sorted_bulletins, downloaded['name'])
            if index != -1 and downloaded['code'] == CME_const.success.value:
                bulletins_insert.append(sorted_bulletins[index])

        self.storage_db.insert_dailybulletin_reports(bulletins_insert)

        return bulletins_insert
