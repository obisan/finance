import ftplib


class CME:

    def __init__(self, host, user, passwd):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.cme = ftplib.FTP(host=self.host, user=self.user, passwd=self.passwd)

    def get_dailybulletin_list(self):
        files = []
        for filename in self.cme.nlst("bulletin"):
            files.append(filename)
        return files

    def download_dailybulletin_by_date(self, date, index):
        filename_src = "bulletin/DailyBulletin_pdf_" + date + index + ".zip"
        # \\192.168.88.10\storage\finance_storage\DailyBulletin
        main_path = "\\\\192.168.88.10\\storage\\finance_storage\\DailyBulletin\\"
        filename_trg = main_path + "DailyBulletin_pdf_" + date + index + ".zip"
        with open(filename_trg, "wb") as file:
            self.cme.retrbinary(f"RETR {filename_src}", file.write)
