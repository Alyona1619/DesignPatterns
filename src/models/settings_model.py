"""
Настройки
"""
from src.core.custom_exception import argument_exception


class settings:
    __organization_name = ""
    __inn = ""
    __account_number = ""
    __correspondent_account = ""
    __bik = ""
    __ownership_type = ""

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