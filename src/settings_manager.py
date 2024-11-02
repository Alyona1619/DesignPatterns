from datetime import datetime

from src.core.custom_exception import argument_exception
from src.models.settings_model import settings
from src.core.abstract_logic import abstract_logic

import json
import os


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
        data.block_period = datetime.now().date().isoformat()

        return data

    def get_block_period(self):
        return self.__settings.block_period

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
            "block_period": self.__settings.block_period
        }

        try:
            with open(file_path, 'w', encoding='utf-8') as stream:
                json.dump(settings_data, stream, ensure_ascii=False, indent=4)
        except Exception as ex:
            self.set_exception(ex)
            raise

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

# Пример использования
# manager1 = settings_manager()
# manager1.open("../settings.json")
# print(f"settings1 {manager1.settings.inn}")
#
# manager2 = settings_manager()
# # manager2.open("settings1.json")
# print(f"settings2 {manager2.settings.inn}")
