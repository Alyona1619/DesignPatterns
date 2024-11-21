from src.core.abstract_reference import abstract_reference
from src.core.validator import validator
from src.dto.filter import filter
from datetime import datetime


class filter_transaction(abstract_reference):
    _nomenclature: filter
    _warehouse: filter
    _start_period: datetime
    _end_period: datetime

    @property
    def warehouse(self) -> filter:
        return self._warehouse

    @warehouse.setter
    def warehouse(self, value: filter):
        if value:
            validator.validate(value, filter)
        self._warehouse = value

    @property
    def nomenclature(self) -> filter:
        return self._nomenclature

    @nomenclature.setter
    def nomenclature(self, value: filter):
        if value:
            validator.validate(value, filter)
        self._nomenclature = value

    @property
    def start_period(self) -> datetime:
        return self._start_period

    @start_period.setter
    def start_period(self, value: datetime):
        self._start_period = value

    @property
    def end_period(self) -> datetime:
        return self._end_period

    @end_period.setter
    def end_period(self, value: datetime):
        self._end_period = value

    def from_json(self, data: dict):
        validator.validate(data, dict)
        try:
            # t_filter = filter_transaction()
            # warehouse_filter = data['warehouse']
            # nomenclature_filter = data['nomenclature']
            # t_filter.start_period = datetime.strptime(data["start_period"], "%Y-%m-%d")
            # t_filter.end_period = datetime.strptime(data["start_period"], "%Y-%m-%d")
            #
            # t_filter.warehouse = filter().from_json(warehouse_filter)
            # t_filter.nomenclature = filter().from_json(nomenclature_filter)
            #
            # return t_filter
            self.start_period = datetime.strptime(data["start_period"], "%Y-%m-%d")
            self.end_period = datetime.strptime(data["end_period"], "%Y-%m-%d")
            self.warehouse = filter().from_json(data['warehouse'])
            self.nomenclature = filter().from_json(data['nomenclature'])
            return self
        except Exception as e:
            raise e

    def set_compare_mode(self, other_object) -> bool:
        pass
