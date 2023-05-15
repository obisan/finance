import configparser
import sys

from db.db_storage import StorageDb

if __name__ == '__main__':
    # host = "ftp.cmegroup.com"
    # user = "anonymous"
    # passwd = "dubinets.av@gmail.com"
    #
    # cme = CME(host, user, passwd)
    #
    # for filename in cme.get_dailybulletin_list():
    #     # bulletin/DailyBulletin_pdf_2023050887.zip
    #     date_pattern = r"(\d{8})(\d+)"
    #     match = re.search(date_pattern, filename)
    #
    #     if match:
    #         print(match.group(1) + " " + match.group(2))

    # cme.download_dailybulletin_by_date(match.group(1), match.group(2))

    config = configparser.ConfigParser()
    config.read('connect.ini')

    storage = \
        StorageDb(
            config['DEFAULT']['host'],
            config['DEFAULT']['port'],
            config['DEFAULT']['dbname'],
            config['DEFAULT']['user'],
            config['DEFAULT']['password'])
    print(storage.get_data()[0][1])

    # connection = mysql_helper()
    # for user_report in connection.get_user_reports():
    #     setting = connection.get_setting(user_report['report_id'])
    #     user_report_axis = connection.get_user_report_axis(user_report['user_report_id'])
    #     user_report_commodity = connection.get_user_report_commodity(user_report['user_report_id'])
    #     futures = futures(user_report, user_report_commodity, user_report_axis, setting, 2019)
    #     code = futures.run()

    sys.exit(0)
