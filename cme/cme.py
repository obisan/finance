import ftplib


class CME:

    def __init__(self, host, user, passwd):
        # url = "https://www.cmegroup.com/ftp/bulletin/DailyBulletin_pdf_20211104213.zip"
        # url = "ftp://ftp.cmegroup.com/bulletin/DailyBulletin_pdf_20210901168.zip"
        self.cme = ftplib.FTP(host=host, user=user, passwd=passwd)

    def get_dailybulletin_list(self):
        files = []
        for filename in self.cme.nlst("bulletin"):
            files.append(filename)
        return files

    def download_dailybulletin_by_date(self, src, dst):
        with open(dst, "wb") as file:
            self.cme.retrbinary(f"RETR {src}", file.write)
        return 0
