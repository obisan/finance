import bisect
import re

from cme.cme import CME
from constants.enums import Setting


class DailybulletinSync:

    def __init__(self, storage_db):
        host = storage_db.get_setting(Setting.CME_FTP_HOST.value)
        user = storage_db.get_setting(Setting.CME_FTP_USER.value)
        passwd = storage_db.get_setting(Setting.CME_FTP_PASSWORD.value)
        self.storage_db = storage_db
        self.host_save_path = storage_db.get_setting(Setting.HOST_SAVE_PATH.value)
        self.host_address = storage_db.get_setting(Setting.HOST_ADDRESS.value)
        self.cme = CME(host, user, passwd)

    def sync_exec(self):
        # bulletin/DailyBulletin_pdf_2023021329.zip
        dailybulletin_list = self.cme.get_dailybulletin_list()

        # 0 'bulletin/DailyBulletin_pdf_2023021329'
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

        # get list values by patterns
        results = [
            [re.search(pattern, filename).group(1) if re.search(pattern, filename) else None
             for pattern in patterns]
            for filename in dailybulletin_list]

        # get records in db by name DailyBulletin_pdf_2023021329, then sort
        dailybulletin_reports_in_db_sorted = \
            sorted(
                [record[1] for record in
                 self.storage_db.get_dailybulletin_reports_by_names(
                     list(map(lambda x: x[1] if isinstance(x, list) else x, results)))],
                key=lambda x: x[1])

        for item in results:
            try:
                target = item[1]
                index = bisect.bisect_left(dailybulletin_reports_in_db_sorted, target, )

                if index != len(dailybulletin_reports_in_db_sorted) \
                        and dailybulletin_reports_in_db_sorted[index] == target:
                    print(f"Found: {dailybulletin_reports_in_db_sorted[index]}")
                    continue
                else:
                    print(f"Not found {target}")

                destination = '/'.join([self.host_save_path, item[2]])

                self.cme.download_dailybulletin_by_date(item[0], destination)
                self.storage_db.insert_dailybulletin_reports(name=item[1], date=item[3], index=item[4],
                                                             path=destination)

                print(f"Loaded & Saved: {target}")
            except Exception as e:
                print("An exception occurred:", e)
                print(f"    {item}")
