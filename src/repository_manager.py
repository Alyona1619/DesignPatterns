import json

from src.core.abstract_logic import abstract_logic
from src.core.event_type import event_type
from src.core.format_reporting import format_reporting
from src.core.validator import validator
from src.data_repository import data_repository
from src.deserializers.json_deserializer import JsonDeserializer
from src.logics.observe_service import observe_service
from src.reports.report_factory import report_factory
from src.settings_manager import settings_manager


class repository_manager(abstract_logic):
    __repository: data_repository = None
    __settings_manager: settings_manager = None
    __data_file: str = "data_repository.json"

    def __init__(self, repository: data_repository, manager: settings_manager) -> None:
        super().__init__()
        validator.validate(repository, data_repository)
        validator.validate(manager, settings_manager)
        self.__repository = repository
        self.__settings_manager = manager

        observe_service.append(self)

    def set_exception(self, ex: Exception):
        """Перегрузка абстрактного метода"""
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)

        if type == event_type.SAVE_DATA:
            self.save_data()
        if type == event_type.LOAD_DATA:
            self.load_data()

    def save_data(self):
        rep_factory = report_factory(self.__settings_manager)
        report = rep_factory.create(format_reporting.JSON)
        try:
            all_reports = {}
            for key, value in self.__repository.data.items():
                if isinstance(value, list):
                    if not value:
                        all_reports[key] = []
                        continue
                    report.create(value)
                    all_reports[key] = json.loads(report.result)
            with open(self.__data_file, "w", encoding="utf-8") as file:
                json.dump(all_reports, file, ensure_ascii=False, indent=2)
        except Exception as ex:
            print(f"Ошибка при сохранении данных (strt_srv): {str(ex)}")

    def load_data(self):
        """Загрузить данные из data_repository.json в репозиторий данных."""
        try:
            with open(self.__data_file, "r", encoding="utf-8") as file:
                data = json.load(file)

                # Инициализируем данные в репозитории
                self.__repository.data[data_repository.blocked_turnover_key()] = [
                    JsonDeserializer.deserialize(item, 'blocked_turnover_model') for item in
                    data.get("blocked_turnover", [])
                ]

                self.__repository.data[data_repository.group_nomenclature_key()] = [
                    JsonDeserializer.deserialize(item, 'group_nomenclature_model') for item in
                    data.get("group_nomenclature", [])
                ]

                self.__repository.data[data_repository.range_key()] = [
                    JsonDeserializer.deserialize(item, 'range_model') for item in data.get("range", [])
                ]

                self.__repository.data[data_repository.nomenclature_key()] = [
                    JsonDeserializer.deserialize(item, 'nomenclature_model') for item in data.get("nomenclature", [])
                ]

                self.__repository.data[data_repository.recipe_key()] = [
                    JsonDeserializer.deserialize(item, 'recipe_model') for item in data.get("recipe", [])
                ]

                self.__repository.data[data_repository.warehouse_key()] = [
                    JsonDeserializer.deserialize(item, 'warehouse_model') for item in data.get("warehouse", [])
                ]

                self.__repository.data[data_repository.transaction_key()] = [
                    JsonDeserializer.deserialize(item, 'warehouse_transaction_model') for item in
                    data.get("transaction", [])
                ]

            print("Данные успешно загружены в репозиторий.")

        except FileNotFoundError:
            print(f"Файл {self.__data_file} не найден.")
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON.")
        except Exception as ex:
            print(f"Ошибка при загрузке данных: {ex}")