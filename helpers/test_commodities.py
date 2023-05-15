from unittest import TestCase

from helpers.database import mysql_helper


class Testcl_commodity_helper(TestCase):
    def test_get_commodity_list(self):
        connection = mysql_helper()
        for line in connection.get_user_report(1):
            print(line)
