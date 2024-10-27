from abc import ABC, abstractmethod
from src.core.format_reporting import format_reporting
from src.core.validator import validator, operation_exception


class abstract_report(ABC):
    """Абстрактный класс для наследования отчетов"""
    __format: format_reporting = format_reporting.CSV
    __result: str = ""

    @abstractmethod
    def create(self, data: list):
        """Сформировать отчет"""
        pass

    @property
    def format(self) -> format_reporting:
        """Тип формата"""
        return self.__format

    @property
    def result(self) -> str:
        """Результат формирования отчета"""
        return self.__result

    @result.setter
    def result(self, value: str):
        validator.validate(value, str)
        self.__result = value

    @staticmethod
    def get_class_fields(first_model, is_callable: bool = False) -> list:
        if not is_callable:
            fields = list(
                filter(
                    lambda x: not x.startswith("_") and x != "attribute_class" and
                              not callable(getattr(first_model.__class__, x)), dir(first_model)
                )
            )
        else:
            fields = list(filter
                          (lambda x: not x.startswith("_") and x != "attribute_class",
                           dir(first_model))
                          )
        return fields
