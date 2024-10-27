from src.core.abstract_reference import abstract_reference
from src.core.validator import validator


class warehouse_model(abstract_reference):
    __name: str = ""
    __address: str = ""

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        validator.validate(value, str, 50)
        self.__name = value.strip()

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str):
        validator.validate(value, str, 255)
        self.__address = value.strip()

    @staticmethod
    def create(name, address):
        item = warehouse_model()
        item.name = name
        item.address = address
        return item

    def set_compare_mode(self, other_object) -> bool:
        pass

    def from_json(self, data):
        validator.validate(data, dict)
        self.name = data.get('name', "")
        self.address = data.get('address', "")
        return self
