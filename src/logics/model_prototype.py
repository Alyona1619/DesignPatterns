from src.core.abstract_prototype import abstract_prototype
from src.dto.filter import filter
from src.dto.filter_by_option import filter_by_option


class model_prototype(abstract_prototype):

    def __init__(self, source: list) -> None:
        super().__init__(source)

    def create(self, data: list, filter_dto: filter):
        super().create(data, filter_dto)
        self.data = self.filter_name(data, filter_dto)
        self.data = self.filter_id(self.data, filter_dto)
        instance = model_prototype(self.data)
        return instance

    @staticmethod
    def filter_name(source: list, filter_dto: filter) -> list:
        if filter_dto.name == "" or filter_dto.name is None:
            return source

        result = []
        for item in source:
            filter_option_instance = filter_by_option(filter_dto.name_filter_option)
            if hasattr(item, 'full_name') and item.full_name and filter_option_instance.filtration(filter_dto.name,
                                                                                                   item.full_name):
                result.append(item)
            elif hasattr(item, 'name') and item.name and filter_option_instance.filtration(filter_dto.name, item.name):
                result.append(item)

        return result

    @staticmethod
    def filter_id(source: list, filter_dto: filter) -> list:
        if filter_dto.id == "" or filter_dto.id is None:
            return source

        result = []
        for item in source:
            filter_option_instance = filter_by_option(filter_dto.id_filter_option)
            if filter_option_instance.filtration(filter_dto.id, str(item.unique_code)):
                result.append(item)

        return result
