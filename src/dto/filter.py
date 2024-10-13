from src.core.abstract_reference import abstract_reference
from src.core.validator import validator
from src.dto.filter_options import filter_option


class filter(abstract_reference):
    __name: str = ""
    __id: str = ""

    __name_filter_option: filter_option = filter_option.EQUAL
    __id_filter_option: filter_option = filter_option.EQUAL

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        validator.validate(value, str, 255)
        self.__name = value

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        validator.validate(value, str, 36)
        self.__id = value

    @property
    def name_filter_option(self) -> filter_option:
        return self.__name_filter_option

    @name_filter_option.setter
    def name_filter_option(self, value: filter_option):
        validator.validate(value, filter_option)
        self.__name_filter_option = value

    @property
    def id_filter_option(self) -> filter_option:
        return self.__id_filter_option

    @id_filter_option.setter
    def id_filter_option(self, value: filter_option):
        validator.validate(value, filter_option)
        self.__id_filter_option = value

    def from_json(self, data):
        """Метод для десериализации объекта filter из JSON."""
        self.name = data.get('name', "")
        self.id = data.get('id', "")
        self.name_filter_option = filter_option[data.get('name_filter_option', '').upper()]
        self.id_filter_option = filter_option[data.get('id_filter_option', '').upper()]
        return self

    def set_compare_mode(self, other_object) -> bool:
        pass
