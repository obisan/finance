from enum import Enum


class Setting(Enum):
    CME_FTP_HOST = "CME_FTP_HOST"
    CME_FTP_USER = "CME_FTP_USER"
    CME_FTP_PASSWORD = "CME_FTP_PASSWORD"
    CME_PRODUCT_URL = "CME_PRODUCT_URL"
    HOST_SAVE_PATH = "HOST_SAVE_PATH"
    HOST_ADDRESS = "HOST_ADDRESS"


class ModeExecution(Enum):
    DAILYBULLETIN_SYNC = "DAILYBULLETIN_SYNC"
    DAILYBULLETIN_SYNC_PRODUCTS = "DAILYBULLETIN_SYNC_PRODUCTS"
    DAILYBULLETIN_ANALYSIS = "DAILYBULLETIN_ANALYSIS"


class DailyBulletinSection(Enum):
    EURO_FX = 39
    EURODOLLAR_CALL = 51
    EURODOLLAR_PUT = 52


class DailybulletinReportsStatus(Enum):
    PROCESSED = 'processed'
    PREPROCESSED = 'preprocessed'
    NOT_DOWNLOADED = 'not_downloaded'
    DOWNLOADED = 'downloaded'


class CME_const(Enum):
    success = '226 Transfer complete.'
    directory_changed = '250 Directory successfully changed.'
