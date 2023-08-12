import unittest

from db import StorageDb
from helpers.helpers import Helper
from log import Logger
from repository import RepositoryBulletin
from scenario import DailybulletinSync


class TestCME(unittest.TestCase):
    def setUp(self) -> None:
        s = 0

    def test01(self):
        settings = Helper.get_settings('config_unittest_sync_bulletin.xml')

        filename = settings['filename']
        repository = settings['repository']

        storage_db = StorageDb(filename=filename)
        repository_bulletin = RepositoryBulletin(repository, Logger())
        dailybulletin_sync = DailybulletinSync(storage_db, repository_bulletin, Logger())
        dailybulletin_sync.sync()
