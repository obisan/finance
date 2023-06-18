from enum import Enum


class Setting(Enum):
    CME_FTP_HOST = "CME_FTP_HOST"
    CME_FTP_USER = "CME_FTP_USER"
    CME_FTP_PASSWORD = "CME_FTP_PASSWORD"
    CME_PRODUCT_URL = "CME_PRODUCT_URL"
    CME_CONTRACT_URL = "CME_CONTRACT_URL"
    HOST_SAVE_PATH = "HOST_SAVE_PATH"
    HOST_ADDRESS = "HOST_ADDRESS"


class ModeExecution(Enum):
    DAILYBULLETIN_SYNC = "DAILYBULLETIN_SYNC"
    DAILYBULLETIN_SYNC_PRODUCTS = "DAILYBULLETIN_SYNC_PRODUCTS"
    DAILYBULLETIN_ANALYSIS = "DAILYBULLETIN_ANALYSIS"
    DAILYBULLETIN_SYNC_CONTRACTS = "DAILYBULLETIN_SYNC_CONTRACTS"


class DailyBulletinSection(Enum):
    EURO_FX = 39
    EURODOLLAR_CALL = 51
    EURODOLLAR_PUT = 52


class DailybulletinReportsStatus(Enum):
    PROCESSED = 'processed'
    PREPROCESSED = 'preprocessed'
    NOT_DOWNLOADED = 'not_downloaded'
    DOWNLOADED = 'downloaded'


class DailyBulletinReportsDataColumns(Enum):
    STRIKE = "STRIKE"
    STRIKE_INDEX = "STRIKE_INDEX"
    OPEN_RANGE = "OPEN RANGE"
    HIGH = "HIGH"
    LOW = "LOW"
    CLOSING_RANGE = "CLOSING RANGE"
    SETT_PRICE = "SETT.PRICE"
    PT_CHGE = "PT.CHGE."
    DELTA = "DELTA"
    EXERCISES = "EXERCISES"
    VOLUME_TRADES_CLEARED = "VOLUME TRADES CLEARED"
    OPEN_INTEREST = "OPEN INTEREST"
    OPEN_INTEREST_DELTA = "OPEN INTEREST DELTA"
    TYPE = "TYPE"


class DailyBulletinSectionsTypes(Enum):
    PUT = 'PUT'
    CALL = 'CALL'
    OTHER = 'OTHER'


class CME_const(Enum):
    success = '226 Transfer complete.'
    directory_changed = '250 Directory successfully changed.'


class ZIP(Enum):
    extracted = 'extracted'
    deleted = 'deleted'
    error = 'error'
