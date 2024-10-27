from abc import ABC, abstractmethod
from src.core.validator import validator


class abstract_prototype(ABC):
    """Абстрактный класс для наследования прототипов"""
    __data = []

    def __init__(self, source: list) -> None:
        super().__init__()
        validator.validate(source, list)
        self.__data = source

    @abstractmethod
    def create(self, data: list, filter):
        validator.validate(data, list)

    @property
    def data(self) -> list:
        return self.__data

    @data.setter
    def data(self, value: list):
        self.__data = value
