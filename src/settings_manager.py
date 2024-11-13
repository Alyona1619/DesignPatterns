import json
import os
from datetime import datetime

from src.core.abstract_logic import abstract_logic
from src.core.custom_exception import argument_exception
from src.core.event_type import event_type
from src.logics.observe_service import observe_service
from src.models.settings_model import settings


class settings_manager(abstract_logic):
    __file_name = "../settings.json"
    __settings: settings = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if self.__settings is None:
            self.__settings = self.__default_settings()

            observe_service.append(self)

    def open(self, file_path: str = ""):
        if not isinstance(file_path, str):
            argument_exception.raise_type_error("file_path", "str")

        if file_path == "":
            file_path = os.path.join(os.curdir, self.__file_name)

        try:
            with open(file_path, 'r', encoding='utf-8') as stream:
                data = json.load(stream)
                self.convert(data)
            return True

        except Exception as ex:
            self.__settings = self.__default_settings()
            self.set_exception(ex)
            return False

    def convert(self, data: dict):
        for key, value in data.items():
            if hasattr(self.__settings, key):
                setattr(self.__settings, key, value)

        if self.__settings.report_settings is None:
            self.__settings.report_settings = {}

    @property
    def current_settings(self) -> settings:
        return self.__settings

    def __default_settings(self):
        data = settings()
        data.inn = "380000000038"
        data.organization_name = "Рога и копыта (default)"
        data.account_number = "12345678901"
        data.correspondent_account = "12345678901"
        data.bik = "123456789"
        data.ownership_type = "ООООО"
        data.block_period = "1900-01-01"
        data.first_start = True

        return data

    def get_block_period_str(self):
        """Возвращает block_period в формате 'YYYY-MM-DD'."""
        if self.__settings.block_period:
            return self.__settings.block_period.strftime("%Y-%m-%d")
        return None

    def get_block_period_date(self):
        """Возвращает block_period в формате datetime."""
        if self.__settings.block_period:
            return self.__settings.block_period
        return None

    def save_settings(self):
        file_path = os.path.join(os.curdir, self.__file_name)

        settings_data = {
            "organization_name": self.__settings.organization_name,
            "inn": self.__settings.inn,
            "account_number": self.__settings.account_number,
            "correspondent_account": self.__settings.correspondent_account,
            "bik": self.__settings.bik,
            "ownership_type": self.__settings.ownership_type,
            "report_settings": self.__settings.report_settings,
            "default_format": self.__settings.default_format.value,
            "block_period": self.__settings.block_period.strftime("%Y-%m-%d"),
            "first_start": self.__settings.first_start
        }

        try:
            with open(file_path, 'w', encoding='utf-8') as stream:
                json.dump(settings_data, stream, ensure_ascii=False, indent=4)
        except Exception as ex:
            self.set_exception(ex)
            raise

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)

        if type == event_type.CHANGE_BLOCK_PERIOD:
            self.save_settings()

        if type == event_type.SAVE_DATA:
            self.current_settings.first_start = False
            self.save_settings()
