from abc import ABC, abstractmethod
import uuid

from src.core.custom_exception import argument_exception

"""
Абстрактный класс для наследования моделей данных
"""


class abstract_reference(ABC):
    __unique_code: str = uuid.uuid4()
    __name: str = ""

    """
    Уникальный код
    """

    @property
    def unique_code(self) -> str:
        return self.__unique_code

    """
    Наименование (с ограничением в 50 символов)
    """

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if len(value) > 50:
            argument_exception.raise_value_error("name", 50)
        self.__name = value

    """
    Вариант сравнения (по коду)
    """

    @abstractmethod
    def set_compare_mode(self, other_object) -> bool:
        if other_object is None: return False
        if not isinstance(other_object, abstract_reference): return False

        return self.__unique_code == other_object.unique_code

    def __eq__(self, value: object) -> bool:
        return self.set_compare_mode(value)