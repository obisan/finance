import unittest

from cme import CME
from db import StorageDb
from helpers.helpers import Helper
from log import Logger
from repository import RepositoryBulletin


class TestCME(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test01(self):
        with open('config_unittest_sync_bulletin.xml', 'r') as file:
            xml_path = file.read()
            settings = Helper.get_settings(xml_path)

            filename = settings['filename']
            repository = settings['repository']

            storage_db = StorageDb(filename=filename)
            repository_bulletin = RepositoryBulletin(repository, Logger())
            cme = CME(storage_db=storage_db, repository=repository_bulletin)
            dailybulletin_list = cme.get_dailybulletin_list()
            self.assertNotEquals(dailybulletin_list, [], 'Error: Empty list from CME ftp.')
