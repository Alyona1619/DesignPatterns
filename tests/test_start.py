from src.settings_manager import settings_manager
from src.start_service import start_service
from src.data_repository import data_repository
import unittest

"""
Набор тестов для проверки работы старта приложения
"""


class TestStart(unittest.TestCase):
    """
    Проверить создание инстанса start_service
    """

    def test_create_start_service(self):
        # Подготовка
        manager = settings_manager()
        manager.open("../settings1.json")
        reposity = data_repository()

        # Действие
        start = start_service(reposity, manager)

        # Проверки
        assert start is not None