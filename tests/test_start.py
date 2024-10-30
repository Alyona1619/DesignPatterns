from src.core.transaction_type import transaction_type
from src.settings_manager import settings_manager
from src.start_service import start_service
from src.data_repository import data_repository
import unittest


class TestStart(unittest.TestCase):
    """Набор тестов для проверки работы старта приложения"""

    def setUp(self):
        """Подготовка тестовой среды перед каждым тестом"""
        self.manager = settings_manager()
        self.manager.open("../settings.json")
        self.repository = data_repository()
        self.start = start_service(self.repository, self.manager)
        self.start.create()

    def test_start_service(self):
        assert self.start is not None

    def test_start_service_create(self):
        assert self.repository.nomenclature_key() in self.repository.data
        assert self.repository.group_key() in self.repository.data
        assert self.repository.range_key() in self.repository.data
        assert self.repository.recipe_key() in self.repository.data
        assert self.repository.warehouse_key() in self.repository.data
        assert self.repository.transaction_key() in self.repository.data

    def test_create_nomenclature_groups(self):
        groups = self.repository.data[self.repository.group_key()]
        assert len(groups) > 0
        assert groups[0].name == 'Заморозка'

    def test_create_nomenclature(self):
        nomenclature_list = self.repository.data[self.repository.nomenclature_key()]
        assert len(nomenclature_list) > 0
        assert nomenclature_list[0].full_name == "Мука пшеничная"
        assert nomenclature_list[1].full_name == "Сахар"

    def test_create_range(self):
        ranges = self.repository.data[self.repository.range_key()]
        assert len(ranges) > 0
        assert ranges[0].name == "грамм"

    def test_create_recipe(self):
        recipe = self.repository.data[self.repository.recipe_key()]
        assert recipe[0].name == 'ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ'
        assert len(recipe[0].ingredients) == 5
        assert recipe[0].ingredients[0].nomenclature.full_name == "Пшеничная мука"
        assert recipe[0].step.startswith('1. Как испечь вафли хрустящие')

    def test_create_warehouse(self):
        warehouses = self.repository.data[self.repository.warehouse_key()]
        assert len(warehouses) > 0, "Склады не были созданы"

        assert warehouses[0].name == "WH1"
        assert warehouses[0].address == "Россия"
        assert warehouses[1].name == "WH2"
        assert warehouses[1].address == "США"

    def test_create_transaction(self):
        transactions = self.repository.data[self.repository.transaction_key()]
        assert len(transactions) == 100, "Транзакции не были созданы или их количество неверное"

        transaction = transactions[0]
        assert transaction.warehouse is not None, "Склад транзакции не установлен"
        assert transaction.nomenclature is not None, "Номенклатура транзакции не установлена"
        assert transaction.quantity > 0, "Количество транзакции должно быть больше 0"
        assert transaction.transaction_type in list(transaction_type), "Неверный тип транзакции"
        assert transaction.range is not None, "Единица измерения транзакции не установлена"
        assert transaction.period is not None, "Период транзакции не установлен"
