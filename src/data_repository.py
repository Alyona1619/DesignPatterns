from src.core.abstract_logic import abstract_logic
from src.core.event_type import event_type


class data_repository(abstract_logic):
    """Репозиторий данных"""
    __data = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(data_repository, cls).__new__(cls)
        return cls.instance

    @property
    def data(self):
        """Набор данных"""
        return self.__data

    @staticmethod
    def group_key() -> str:
        """Ключ для хранения групп номенклатуры"""
        return "group"

    @staticmethod
    def nomenclature_key() -> str:
        """Ключ для хранения номенклатуры"""
        return "nomenclature"

    @staticmethod
    def range_key() -> str:
        """Ключ для хранения единиц измерения"""
        return "range"

    @staticmethod
    def recipe_key() -> str:
        """Ключ для хранения рецептов"""
        return "recipes"

    @staticmethod
    def warehouse_key() -> str:
        """Ключ для хранения складов"""
        return "warehouses"

    @staticmethod
    def transaction_key() -> str:
        """Ключ для хранения транзакций"""
        return "transactions"

    @staticmethod
    def blocked_turnover_key() -> str:
        """Ключ для хранения заблокированных оборотов"""
        return "blocked_turnover"

    def set_exception(self, ex: Exception):
        """Перегрузка абстрактного метода"""
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)
