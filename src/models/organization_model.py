from DesignPatterns.src.abstract_reference import abstract_reference
from DesignPatterns.src.custom_exception import argument_exception
from DesignPatterns.src.models.settings_model import settings


class organization_model(abstract_reference):
    __inn = ""
    __bik = ""
    __account_number = ""
    __ownership_type = ""

    def __init__(self):
        super().__init__()

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
    def ownership_type(self):
        return self.__ownership_type

    @ownership_type.setter
    def ownership_type(self, value: str):
        if not isinstance(value, str):
            argument_exception.raise_type_error("ownership_type", "str")
        if len(value) != 5:
            argument_exception.raise_value_error("ownership_type", 5)
        self.__ownership_type = value

    def from_settings(self, settings: settings):
        self.inn = settings.inn
        self.account_number = settings.account_number
        self.bik = settings.bik
        self.ownership_type = settings.ownership_type

    def set_compare_mode(self, other_object) -> bool:
        if not isinstance(other_object, organization_model):
            return False
        return super().set_compare_mode(other_object)
