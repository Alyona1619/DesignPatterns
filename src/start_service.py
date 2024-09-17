from src.core.abstract_logic import abstract_logic
from src.data_repository import data_repository
from src.core.validator import validator
from src.models.group_nomenclature_model import group_nomenclature_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.settings_manager import settings_manager
from src.models.settings_model import settings

"""
Сервис для реализации первого старта приложения
"""


class start_service(abstract_logic):
    __repository: data_repository = None
    __settings_manager: settings_manager = None

    def __init__(self, repository: data_repository, manager: settings_manager) -> None:
        super().__init__()
        validator.validate(repository, data_repository)
        validator.validate(manager, settings_manager)
        self.__repository = repository
        self.__settings_manager = manager

    """
    Текущие настройки
    """

    @property
    def settings(self) -> settings:
        return self.__settings_manager.current_settings

    """
    Сформировать группы номенклатуры
    """

    def __create_nomenclature_groups(self):
        list = []
        list.append(group_nomenclature_model.default_group_cold())
        list.append(group_nomenclature_model.default_group_source())
        self.__repository.data[data_repository.group_key()] = list

    """
    Сформировать номенклатуру
    """

    def __create_nomenclature(self):
        nomenclature_list = []
        nomenclature_item1 = nomenclature_model()
        nomenclature_item1.full_name = "Номенклатура 1"
        nomenclature_list.append(nomenclature_item1)

        nomenclature_item2 = nomenclature_model()
        nomenclature_item2.full_name = "Номенклатура 2"
        nomenclature_list.append(nomenclature_item2)

        self.__repository.data[data_repository.nomenclature_key()] = nomenclature_list

    """
    Сформировать единицы измерения
    """

    def __create_range(self):
        range_list = []
        range_item1 = range_model()
        range_item1.name = "грамм"
        range_item1.coef = 1.0
        range_list.append(range_item1)

        range_item2 = range_model()
        range_item2.name = "килограмм"
        range_item2.coef = 1000.0
        range_list.append(range_item2)

        self.__repository.data[data_repository.range_key()] = range_list

    """
    Первый старт
    """

    def create(self):
        self.__create_nomenclature_groups()
        self.__create_range()
        self.__create_nomenclature()

    """
    Перегрузка абстрактного метода
    """

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
