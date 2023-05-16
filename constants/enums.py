from enum import Enum


class Setting(Enum):
    CME_FTP_HOST = "CME_FTP_HOST"
    CME_FTP_USER = "CME_FTP_USER"
    CME_FTP_PASSWORD = "CME_FTP_PASSWORD"


class ModeExecution(Enum):
    DAILYBULLETIN_SYNC = "DAILYBULLETIN_SYNC"
