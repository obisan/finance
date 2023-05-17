import ftplib


class CME:

    def __init__(self, host, user, passwd):
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
