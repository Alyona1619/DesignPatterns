from src.core.abstract_logic import abstract_logic

"""
Репозиторий данных
"""


class data_repository(abstract_logic):
    __data = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(data_repository, cls).__new__(cls)
        return cls.instance

    """
    Набор данных
    """

    @property
    def data(self):
        return self.__data

    """
    Ключ для хранения групп номенклатуры
    """

    @staticmethod
    def group_key() -> str:
        return "group"

    """
    Ключ для хранения номенклатуры
    """

    @staticmethod
    def nomenclature_key() -> str:
        return "nomenclature"

    """
    Ключ для хранения единиц измерения
    """

    @staticmethod
    def range_key() -> str:
        return "range"

    """
    Ключ для хранения рецептов
    """

    @staticmethod
    def recipe_key() -> str:
        return "recipes"

    """
    Перегрузка абстрактного метода
    """

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
