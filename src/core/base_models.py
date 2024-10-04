from src.core.abstract_reference import abstract_reference
from src.core.validator import validator

"""
Базовый класс для наследования с поддержкой сравнения по коду
"""


class base_model_code(abstract_reference):
    def set_compare_mode(self, other_object) -> bool:
        return super().set_compare_mode(other_object)

    def from_json(self, data):
        pass

"""
Базовый класс для наследования с поддержкой сравнения по наименованию
"""


class base_model_name(abstract_reference):
    __name: str = ""

    @property
    def name(self) -> str:
        return self.__name.strip()

    @name.setter
    def name(self, value: str):
        validator.validate(value, str, 255)
        self.__name = value

    def set_compare_mode(self, other_object: 'base_model_name') -> bool:
        if other_object is None: return False
        if not isinstance(other_object, base_model_name): return False

        return self.name == other_object.name

    def from_json(self, data):
        pass
