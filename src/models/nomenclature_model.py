from src.core.abstract_reference import abstract_reference
from src.core.custom_exception import argument_exception
from src.models.group_nomenclature_model import group_nomenclature_model
from src.models.range_model import range_model


class nomenclature_model(abstract_reference):
    """Модель номенклатуры"""
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
    def unit(self) -> range_model:
        return self.__unit

    @unit.setter
    def unit(self, value: range_model):
        self.__unit = value

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)

    @staticmethod
    def default_nomenclature(full_name, group, unit):
        nomenclature = nomenclature_model()
        nomenclature.full_name = full_name
        nomenclature.group = group
        nomenclature.unit = unit
        return nomenclature

    # @staticmethod
    # def from_json(data):
    #     """Фабричный метод для десериализации номенклатуры из JSON."""
    #     nomenclature_instance = nomenclature_model()
    #     nomenclature_instance.full_name = data.get('full_name', '')
    #     nomenclature_instance.group = group_nomenclature_model.from_json(data['group'])
    #     nomenclature_instance.unit = range_model.from_json(data['unit'])
    #     return nomenclature_instance

    def from_json(self, data):
        self.full_name = data.get('full_name', '')
        self.group = group_nomenclature_model().from_json(data['group'])
        self.unit = range_model().from_json(data['unit'])
        return self
