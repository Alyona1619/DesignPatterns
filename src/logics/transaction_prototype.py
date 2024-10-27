from src.core.validator import validator
from src.dto.filter_transaction import filter_transaction
from src.dto.filter import filter
from src.logics.model_prototype import model_prototype
from src.dto.filter_by_option import filter_by_option
from datetime import datetime


class transaction_prototype(model_prototype):

    def __init__(self, source: list) -> None:
        super().__init__(source)

    def create(self, data: list, filter_transaction: filter_transaction):
        self.data = data
        if filter_transaction.warehouse:
            self.data = self.filter_id(self.data, filter_transaction.warehouse)
            self.data = self.filter_name(self.data, filter_transaction.warehouse)
        if filter_transaction.nomenclature:
            self.data = self.filter_id(self.data, filter_transaction.nomenclature)
            self.data = self.filter_name(self.data, filter_transaction.nomenclature)

        if filter_transaction.start_period and filter_transaction.end_period:
            self.data = self.filter_period(self.data, filter_transaction.start_period,
                                           filter_transaction.end_period)

        return transaction_prototype(data)

    @staticmethod
    def filter_id(source: list, filter_dto: filter) -> list:
        if filter_dto.id is None or filter_dto.id == "":
            return source

        result = []
        for item in source:
            filter_option_instance = filter_by_option(filter_dto.filter_option)
            if filter_option_instance.filtration(filter_dto.id, str(item.unique_code)):
                result.append(item)

        return result

    @staticmethod
    def filter_name(source: list, filter_dto: filter) -> list:
        if filter_dto.name == "" or filter_dto.name is None:
            return source

        result = []
        for item in source:
            filter_option_instance = filter_by_option(filter_dto.filter_option)
            if hasattr(item, 'full_name') and item.full_name and filter_option_instance.filtration(filter_dto.name,
                                                                                                   item.full_name):
                result.append(item)
            elif hasattr(item, 'name') and item.name and filter_option_instance.filtration(filter_dto.name, item.name):
                result.append(item)

        return result

    @staticmethod
    def filter_period(source: list, start_period: datetime, end_period: datetime) -> list:
        validator.validate(source, list)
        validator.validate(start_period, datetime)
        validator.validate(end_period, datetime)
        filter_data = []
        for item in source:
            if start_period <= getattr(item, "period") <= end_period:
                filter_data.append(item)
        return filter_data
