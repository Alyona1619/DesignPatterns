import json

from src.core.abstract_logic import abstract_logic
from src.core.event_type import event_type


class data_repository(abstract_logic):
    """Репозиторий данных"""
    __data = {}

    # instance: 'data_repository' = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(data_repository, cls).__new__(cls)
        return cls.instance

    @property
    def data(self):
        """Набор данных"""
        return self.__data

    @staticmethod
    def group_nomenclature_key() -> str:
        """Ключ для хранения групп номенклатуры"""
        return "group_nomenclature"

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
        return "recipe"

    @staticmethod
    def warehouse_key() -> str:
        """Ключ для хранения складов"""
        return "warehouse"

    @staticmethod
    def transaction_key() -> str:
        """Ключ для хранения транзакций"""
        return "transaction"

    @staticmethod
    def blocked_turnover_key() -> str:
        """Ключ для хранения заблокированных оборотов"""
        return "blocked_turnover"

    def set_exception(self, ex: Exception):
        """Перегрузка абстрактного метода"""
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, rep_factory):
        super().handle_event(type, rep_factory)

        if type == event_type.SAVE_DATA:
            try:
                all_reports = {}
                for key, value in self.__data.items():
                    if isinstance(value, list):
                        report = rep_factory.create_default()
                        report.create(value)
                        all_reports[key] = report.result

                with open("repository_data.json", "w", encoding="utf-8") as file:
                    json.dump(all_reports, file, ensure_ascii=False, indent=2)
            except Exception as ex:
                print(f"Ошибка при сохранении данных: {str(ex)}")

        if type == event_type.LOAD_DATA:
            pass
