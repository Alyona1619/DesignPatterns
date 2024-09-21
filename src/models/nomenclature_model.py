from src.core.abstract_reference import abstract_reference
from src.core.custom_exception import argument_exception
from src.models.group_nomenclature_model import group_nomenclature_model
from src.models.range_model import range_model

"""
Модель номенклатуры
"""

class nomenclature_model(abstract_reference):
    __full_name: str = ''
    __group: group_nomenclature_model = None
    __unit: range_model = None

    def __init__(self):
        super().__init__()

    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str):
        if len(value) > 255:
            argument_exception.raise_value_error("full_name", 255)
        self.__full_name = value

    @property
    def group(self) -> group_nomenclature_model:
        return self.__group

    @group.setter
    def group(self, value: group_nomenclature_model):
        self.__group = value

    @property
    def range(self) -> range_model:
        return self.__unit

    @range.setter
    def range(self, value: range_model):
        self.__unit = value

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)

    @staticmethod
    def default_nomenclature(full_name, group):
        nomenclature = nomenclature_model()
        nomenclature.full_name = full_name
        nomenclature.group = group
        return nomenclature
