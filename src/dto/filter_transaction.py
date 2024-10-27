from src.core.abstract_reference import abstract_reference
from src.core.validator import validator
from src.dto.filter import filter
from datetime import datetime


class filter_transaction(abstract_reference):
    __nomenclature: filter
    __warehouse: filter
    __start_period: datetime
    __end_period: datetime

    @property
    def warehouse(self) -> filter:
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: filter):
        validator.validate(value, filter)
        self.__warehouse = value

    @property
    def nomenclature(self) -> filter:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: filter):
        validator.validate(value, filter)
        self.__nomenclature = value

    @property
    def start_period(self) -> datetime:
        return self.__start_period

    @start_period.setter
    def start_period(self, value: datetime):
        self.__start_period = value

    @property
    def end_period(self) -> datetime:
        return self.__end_period

    @end_period.setter
    def end_period(self, value: datetime):
        self.__end_period = value

    def from_json(self, data: dict):
        validator.validate(data, dict)
        try:
            t_filter = filter_transaction()
            warehouse_filter = data['warehouse']
            nomenclature_filter = data['nomenclature']
            t_filter.start_period = datetime.strptime(data["start_period"], "%Y-%m-%d")
            t_filter.end_period = datetime.strptime(data["start_period"], "%Y-%m-%d")

            t_filter.warehouse = filter().from_json(warehouse_filter)
            t_filter.nomenclature = filter().from_json(nomenclature_filter)

            return t_filter
        except Exception as e:
            raise e

    def set_compare_mode(self, other_object) -> bool:
        pass
