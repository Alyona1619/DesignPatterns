from src.core.abstract_reference import abstract_reference
from src.core.validator import validator
from src.models.warehouse_model import warehouse_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model

class warehouse_turnover_model(abstract_reference):
    __warehouse: warehouse_model
    __turnover: float = 0.0
    __nomenclature: nomenclature_model
    __range: range_model

    @property
    def warehouse(self) -> warehouse_model:
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: warehouse_model):
        validator.validate(value, warehouse_model)
        self.__warehouse = value

    @property
    def turnover(self) -> float:
        return self.__turnover

    @turnover.setter
    def turnover(self, value: float):
        validator.validate(value, float)
        self.__turnover = value

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value: range_model):
        validator.validate(value, range_model)
        self.__range = value

    @staticmethod
    def create(warehouse: warehouse_model, nomenclature: nomenclature_model, range: range_model, turnover: float = 0.0):
        wh_to = warehouse_turnover_model()
        wh_to.warehouse = warehouse
        wh_to.nomenclature = nomenclature
        wh_to.range = range
        wh_to.turnover = turnover
        return wh_to

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)

    def from_json(self, data):
        pass

