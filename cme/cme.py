import ftplib
import os

from constants.enums import CME_const
from constants.enums import Setting


class CME:

    def __init__(self, host=None, user=None, passwd=None, storage_db=None, repository=None):
        # url = "https://www.cmegroup.com/ftp/bulletin/DailyBulletin_pdf_20211104213.zip"
        # url = "ftp://ftp.cmegroup.com/bulletin/DailyBulletin_pdf_20210901168.zip"
        if storage_db:
            self._init_from_storage(storage_db)
        else:
            self._init_from_credentials(host, user, passwd)

        self.repository = repository

    def _init_from_storage(self, storage_db):
        host = storage_db.get_setting(Setting.CME_FTP_HOST.value)
        user = storage_db.get_setting(Setting.CME_FTP_USER.value)
        passwd = storage_db.get_setting(Setting.CME_FTP_PASSWORD.value)

        self._init_from_credentials(host, user, passwd)

    def _init_from_credentials(self, host, user, passwd):
        self.cme = ftplib.FTP(host=host, user=user, passwd=passwd)

    def get_dailybulletin_list(self):
        files = []
        for filename in self.cme.nlst("bulletin"):
            files.append(filename)
        return files

    def download_dailybulletins_by_name(self, names):
        result = []
        if self.cme.cwd("/bulletin") != CME_const.directory_changed.value:
            raise Exception("Can not change directory on ftp cme")
        for name in names:
            src = name + '.zip'
            dst = os.path.join(self.repository.path, name) + '.zip'
            with open(dst, "wb") as file:
                code = self.cme.retrbinary(f"RETR {src}", file.write)
                result.append({
                    'name': name,
                    'code': code
                })
        self.cme.cwd("/")
        return result
