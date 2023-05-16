import re

from cme.cme import CME
from constants.enums import Setting


class DailybulletinSync:

    def __init__(self, storage_db):
        host = storage_db.get_setting(Setting.CME_FTP_HOST.value)
        user = storage_db.get_setting(Setting.CME_FTP_USER.value)
        passwd = storage_db.get_setting(Setting.CME_FTP_PASSWORD.value)
        self.cme = CME(host, user, passwd)

    def sync_exec(self):
        for filename in self.cme.get_dailybulletin_list():
            # bulletin/DailyBulletin_pdf_2023050887.zip
            date_pattern = r"(\d{8})(\d+)"
            match = re.search(date_pattern, filename)

            if match:
                print(match.group(1) + " " + match.group(2))

        # cme.download_dailybulletin_by_date(match.group(1), match.group(2))

        # storage.insert_dailybulletin_reports()
