from enum import Enum


class event_type(Enum):
    """Типы событий"""
    DELETE_NOMENCLATURE = 1
    CHANGE_NOMENCLATURE = 2
    CHANGE_NOMENCLATURE_IN_RECIPE = 3
    CHANGE_NOMENCLATURE_IN_TURNOVER = 4
    CHANGE_RANGE = 5
    CHANGE_BLOCK_PERIOD = 6
    SAVE_DATA = 7
    LOAD_DATA = 8

    LOG_INFO = 9
    LOG_ERROR = 10
    LOG_DEBUG = 11

