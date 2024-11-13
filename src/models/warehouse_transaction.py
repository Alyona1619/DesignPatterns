from src.core.abstract_reference import abstract_reference
from src.core.transaction_type import transaction_type
from src.core.validator import validator
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.warehouse_model import warehouse_model
from datetime import datetime


class warehouse_transaction_model(abstract_reference):
    __warehouse: warehouse_model
    __nomenclature: nomenclature_model
    __quantity: float = 0.0
    __transaction_type: transaction_type
    __range: range_model
    __period: datetime

    @property
    def warehouse(self) -> warehouse_model:
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: warehouse_model):
        validator.validate(value, warehouse_model)
        self.__warehouse = value

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        # validator
        self.__quantity = value

    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value: range_model):
        validator.validate(value, range_model)
        self.__range = value

    @property
    def period(self) -> datetime:
        return self.__period

    @period.setter
    def period(self, value: datetime):
        validator.validate(value, datetime)
        self.__period = value

    @property
    def transaction_type(self) -> transaction_type:
        return self.__transaction_type

    @transaction_type.setter
    def transaction_type(self, value: transaction_type):
        validator.validate(value, transaction_type)
        self.__transaction_type = value

    @staticmethod
    def create(warehouse: warehouse_model, nomenclature: nomenclature_model, quantity: float,
               range: range_model, period: datetime,
               transaction_type: transaction_type) -> 'warehouse_transaction_model':
        transaction = warehouse_transaction_model()
        transaction.warehouse = warehouse
        transaction.nomenclature = nomenclature
        transaction.quantity = quantity
        transaction.range = range
        transaction.period = period
        transaction.transaction_type = transaction_type
        return transaction

    def set_compare_mode(self, other_object):
        super().set_compare_mode(other_object)

    def from_json(self, data):
        self.warehouse = warehouse_model().from_json(data['warehouse'])
        self.nomenclature = nomenclature_model().from_json(data['nomenclature'])
        self.quantity = data.get('quantity', 0.0)
        self.range = range_model().from_json(data['range'])
        self.period = datetime.strptime(data['period'],
                                        '%Y-%m-%dT%H:%M:%S') if 'period' in data else None
        self.transaction_type = transaction_type[
            data['transaction_type']] if 'transaction_type' in data else None
        return self
