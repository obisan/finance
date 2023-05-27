from enum import Enum


class Setting(Enum):
    CME_FTP_HOST = "CME_FTP_HOST"
    CME_FTP_USER = "CME_FTP_USER"
    CME_FTP_PASSWORD = "CME_FTP_PASSWORD"
    HOST_SAVE_PATH = "HOST_SAVE_PATH"
    HOST_ADDRESS = "HOST_ADDRESS"


class ModeExecution(Enum):
    DAILYBULLETIN_SYNC = "DAILYBULLETIN_SYNC"
    DAILYBULLETIN_ANALYSIS = "DAILYBULLETIN_ANALYSIS"


class DailyBulletinSection(Enum):
    EURO_DOLLAR_CALL = 53
    EURO_DOLLAR_PUT = 54
