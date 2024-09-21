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

    def test_start_service(self):
        # Подготовка
        manager = settings_manager()
        manager.open("../settings1.json")
        reposity = data_repository()

        # Действие
        start = start_service(reposity, manager)

        # Проверки
        assert start is not None

    def test_start_service_create(self):
        manager = settings_manager()
        manager.open("../settings1.json")
        repository = data_repository()

        start = start_service(repository, manager)
        start.create()

        assert repository.nomenclature_key() in repository.data
        assert repository.group_key() in repository.data
        assert repository.range_key() in repository.data
        assert repository.recipe_key() in repository.data

    def test_create_nomenclature_groups(self):
        manager = settings_manager()
        repository = data_repository()
        start = start_service(repository, manager)

        start.create()

        groups = repository.data[repository.group_key()]
        assert len(groups) > 0
        assert groups[0].name == 'Заморозка'

    def test_create_nomenclature(self):
        manager = settings_manager()
        repository = data_repository()
        start = start_service(repository, manager)

        start.create()

        nomenclature_list = repository.data[repository.nomenclature_key()]
        assert len(nomenclature_list) > 0
        assert nomenclature_list[0].full_name == "Мука пшеничная"
        assert nomenclature_list[1].full_name == "Сахар"

    def test_create_range(self):
        manager = settings_manager()
        repository = data_repository()
        start = start_service(repository, manager)

        start.create()

        ranges = repository.data[repository.range_key()]
        assert len(ranges) > 0
        assert ranges[0].name == "грамм"

    def test_create_recipe(self):
        manager = settings_manager()
        repository = data_repository()
        start = start_service(repository, manager)

        start.create()

        recipe = repository.data[repository.recipe_key()]
        assert recipe.name == 'ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ'
        assert len(recipe.ingredients) == 5
        assert recipe.ingredients[0].nomenclature.full_name == "Пшеничная мука"
        assert recipe.step.startswith('1. Как испечь вафли хрустящие')

