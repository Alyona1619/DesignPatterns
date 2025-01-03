from enum import Enum


class format_reporting(Enum):
    """Форматы отчетов"""
    CSV = 1
    MARKDOWN = 2
    JSON = 3
    XML = 4
    RTF = 5
    TBS = 6  # turnover-balance sheet
    TXT = 7
