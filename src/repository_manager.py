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
        # генерация data_map для ключей, соответствующих общему принципу (_key, _model)
        data_methods = [method for method in dir(data_repository)
                        if callable(getattr(data_repository, method)) and method.endswith('_key')]

        data_map = {
            getattr(data_repository, method)(): (method.replace('_key', ''), f"{method.replace('_key', '')}_model")
            for method in data_methods
            if method not in ('blocked_turnover_key', 'transaction_key')
        }

        # исключения
        data_map[data_repository.blocked_turnover_key()] = ("blocked_turnover", "warehouse_turnover_model")
        data_map[data_repository.transaction_key()] = ("transaction", "warehouse_transaction_model")

        try:
            with open(self.__data_file, "r", encoding="utf-8") as file:
                data = json.load(file)

                for key, (data_key, model_name) in data_map.items():
                    self.__repository.data[key] = [
                        JsonDeserializer.deserialize(item, model_name) for item in data.get(data_key, [])
                    ]

            print("Данные успешно загружены в репозиторий.")

        except FileNotFoundError:
            print(f"Файл {self.__data_file} не найден.")
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON.")
        except Exception as ex:
            print(f"Ошибка при загрузке данных: {ex}")