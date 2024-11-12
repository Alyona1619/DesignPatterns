from datetime import datetime

from src.core.custom_exception import argument_exception
from src.core.format_reporting import format_reporting
from src.core.validator import validator


class settings:
    """Настройки"""
    __organization_name = ""
    __inn = ""
    __account_number = ""
    __correspondent_account = ""
    __bik = ""
    __ownership_type = ""
    __report_format = format_reporting.JSON
    __report_settings: dict = None
    __default_format: format_reporting = format_reporting.JSON
    __block_period: datetime
    __first_start: bool = True

    @property
    def organization_name(self):
        return self.__organization_name

    @organization_name.setter
    def organization_name(self, value: str):
        if not isinstance(value, str):
            argument_exception.raise_type_error("organization_name", "str")
        self.__organization_name = value

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str):
            argument_exception.raise_type_error("inn", "str")
        if len(value) != 12:
            argument_exception.raise_value_error("inn", 12)
        self.__inn = value

    @property
    def account_number(self):
        return self.__account_number

    @account_number.setter
    def account_number(self, value: str):
        if not isinstance(value, str):
            argument_exception.raise_type_error("account_number", "str")
        if len(value) != 11:
            argument_exception.raise_value_error("account_number", 11)
        self.__account_number = value

    @property
    def correspondent_account(self):
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value: str):
        if not isinstance(value, str):
            argument_exception.raise_type_error("correspondent_account", "str")
        if len(value) != 11:
            argument_exception.raise_value_error("correspondent_account", 11)
        self.__correspondent_account = value

    @property
    def bik(self):
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        if not isinstance(value, str):
            argument_exception.raise_type_error("bik", "str")
        if len(value) != 9:
            argument_exception.raise_value_error("bik", 9)
        self.__bik = value

    @property
    def ownership_type(self):
        return self.__ownership_type

    @ownership_type.setter
    def ownership_type(self, value: str):
        if not isinstance(value, str):
            argument_exception.raise_type_error("ownership_type", "str")
        if len(value) != 5:
            argument_exception.raise_value_error("ownership_type", 5)
        self.__ownership_type = value

    @property
    def report_format(self) -> format_reporting:
        return self.__report_format

    @report_format.setter
    def report_format(self, value: format_reporting):
        if not isinstance(value, format_reporting):
            argument_exception.raise_type_error("report_format", "format_reporting")
        self.__report_format = value

    @property
    def report_settings(self):
        return self.__report_settings

    @report_settings.setter
    def report_settings(self, value: dict):
        self.__report_settings = value

    @property
    def default_format(self):
        return self.__default_format

    @default_format.setter
    def default_format(self, value: format_reporting):
        if not isinstance(value, int):
            argument_exception.raise_type_error("default_format", "int")

        try:
            self.__default_format = format_reporting(value)
        except ValueError:
            argument_exception.raise_value_error("default_format", "valid format integer (1-6)")

    @property
    def block_period(self):
        return self.__block_period

    @block_period.setter
    def block_period(self, value: str):
        if isinstance(value, datetime):
            value = value.strftime("%Y-%m-%d")
        elif not isinstance(value, str):
            argument_exception.raise_type_error("block_period", "str or datetime")

        validator.validate(value, str, 12)
        self.__block_period = datetime.strptime(value, "%Y-%m-%d")

    @property
    def first_start(self):
        return self.__first_start

    @first_start.setter
    def first_start(self, value: bool):
        validator.validate(value, bool)
        self.__first_start = value
