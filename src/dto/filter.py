from src.core.abstract_reference import abstract_reference
from src.core.validator import validator
from src.core.filter_options import filter_option


class filter(abstract_reference):
    __name: str = ""
    __id: str = ""
    __filter_option: filter_option = filter_option.LIKE

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if value:
            validator.validate(value, str, 255)
        self.__name = value

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        validator.validate(value, str, 37)
        self.__id = value

    @property
    def filter_option(self) -> filter_option:
        return self.__filter_option

    @filter_option.setter
    def filter_option(self, value: filter_option):
        validator.validate(value, filter_option)
        self.__filter_option = value

    def from_json(self, data):
        """Метод для десериализации объекта filter из JSON."""
        # try:
        #     if 'name' in data:
        #         self.name = data['name']
        #     if 'id' in data:
        #         self.id = data['id']
        #     if 'filter_option' in data:
        #         self.filter_option = filter_option[data.get('filter_option', 'LIKE').upper()]
        #     return self
        # except Exception as e:
        #     raise f"{e}"
        validator.validate(data, dict)
        try:
            self.name = data.get('name', "")
            self.id = data.get('id', "")
            self.filter_option = filter_option[data.get('filter_option', 'LIKE').upper()]
            return self
        except Exception as e:
            raise e

    def set_compare_mode(self, other_object) -> bool:
        pass
