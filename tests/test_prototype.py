import unittest

from src.dto.filter_options import filter_option
from src.logics.model_prototype import model_prototype
from src.dto.filter import filter
from src.data_repository import data_repository
from src.settings_manager import settings_manager
from src.start_service import start_service


class test_prototype(unittest.TestCase):
    """Набор тестов для проверки прототипов"""

    def setUp(self):
        """Подготовка тестовой среды перед каждым тестом"""
        self.manager = settings_manager()
        self.manager.open("../settings.json")
        self.repository = data_repository()
        self.start = start_service(self.repository, self.manager)
        self.start.create()

    def test_prototype_nomenclature_eq(self):
        if len(self.repository.data[data_repository.nomenclature_key()]) == 0:
            raise Exception("Нет данных!")
        # Подготовка
        data = self.repository.data[data_repository.nomenclature_key()]
        item = data[0]
        item_filter = filter()
        item_filter.name = item.full_name
        prototype = model_prototype(data)

        # Действие
        result = prototype.create(data, item_filter)

        # Проверка
        assert len(result.data) == 1
        assert result.data[0] == item

    def test_prototype_range_eq(self):
        if len(self.repository.data[data_repository.range_key()]) == 0:
            raise Exception("Нет данных!")
        # Подготовка
        data = self.repository.data[data_repository.range_key()]
        item = data[0]
        item_filter = filter()
        item_filter.name = item.name
        prototype = model_prototype(data)

        # Действие
        result = prototype.create(data, item_filter)

        # Проверка
        assert len(result.data) == 1
        assert result.data[0] == item

    def test_prototype_group_eq(self):
        if len(self.repository.data[data_repository.group_key()]) == 0:
            raise Exception("Нет данных!")
        # Подготовка
        data = self.repository.data[data_repository.group_key()]
        item = data[0]
        item_filter = filter()
        item_filter.name = item.name
        prototype = model_prototype(data)

        # Действие
        result = prototype.create(data, item_filter)

        # Проверка
        assert len(result.data) == 1
        assert result.data[0] == item

    def test_prototype_recipe_eq(self):
        if len(self.repository.data[data_repository.recipe_key()]) == 0:
            raise Exception("Нет данных!")

            # Подготовка
        data = self.repository.data[data_repository.recipe_key()]
        item = data[0]
        item_filter = filter()
        item_filter.name = item.name
        prototype = model_prototype(data)

        # Действие
        result = prototype.create(data, item_filter)

        # Проверка
        assert len(result.data) == 1
        assert result.data[0] == item

    def test_prototype_nomenclature_like(self):

        if len(self.repository.data[data_repository.nomenclature_key()]) == 0:
            raise Exception("Нет данных!")
        # Подготовка
        data = self.repository.data[data_repository.nomenclature_key()]
        item_filter = filter()
        item_filter.name = "а"
        item_filter.name_filter_option = filter_option.LIKE
        prototype = model_prototype(data)

        # Действие
        prototype.create(data, item_filter)

        # Проверка
        assert len(prototype.data) > 1

    def test_prototype_group_like(self):
        if len(self.repository.data[data_repository.group_key()]) == 0:
            raise Exception("Нет данных!")
        # Подготовка
        data = self.repository.data[data_repository.group_key()]
        item_filter = filter()
        item_filter.name = "ь"
        item_filter.name_filter_option = filter_option.LIKE
        prototype = model_prototype(data)

        # Действие
        prototype.create(data, item_filter)

        # Проверка
        assert len(prototype.data) >= 1

    def test_prototype_range_like(self):
        if len(self.repository.data[data_repository.range_key()]) == 0:
            raise Exception("Нет данных!")
        # Подготовка
        data = self.repository.data[data_repository.range_key()]
        item_filter = filter()
        item_filter.name = "т"
        item_filter.name_filter_option = filter_option.LIKE
        prototype = model_prototype(data)

        # Действие
        prototype.create(data, item_filter)

        # Проверка
        assert len(prototype.data) == 1

    def test_prototype_recipe_like(self):
        if len(self.repository.data[data_repository.recipe_key()]) == 0:
            raise Exception("Нет данных!")
        # Подготовка
        data = self.repository.data[data_repository.recipe_key()]
        item_filter = filter()
        item_filter.name = "ВАФ"
        item_filter.name_filter_option = filter_option.LIKE
        prototype = model_prototype(data)

        # Действие
        prototype.create(data, item_filter)

        # Проверка
        assert len(prototype.data) == 1

    def test_id_equale(self):
        # Подготовка
        if len(self.repository.data[data_repository.nomenclature_key()]) == 0:
            raise Exception("Нет данных!")

        data = self.repository.data[data_repository.nomenclature_key()]
        item = data[0]
        item_filter = filter()
        item_filter.id = str(item.unique_code)
        prototype = model_prototype(data)

        # Действие
        result = prototype.create(data, item_filter)
        print(result.data)
        # Проверка
        assert len(result.data) == 1
        assert prototype.data[0] == item

    def test_id_like(self):
        # Подготовка
        if len(self.repository.data[data_repository.nomenclature_key()]) == 0:
            raise Exception("Нет данных!")

        data = self.repository.data[data_repository.nomenclature_key()]
        item = data[0]
        item_filter = filter()
        item_filter.id = str(item.unique_code)[:3]
        item_filter.id_filter_option = filter_option.LIKE
        prototype = model_prototype(data)

        # Действие
        prototype.create(data, item_filter)

        # Проверка
        assert len(prototype.data) >= 1
        assert prototype.data[0] == item
