from src.dto.filter_options import filter_option


class filter:
    __name: str = ""
    __id: str = ""

    __name_filter_option: filter_option = filter_option.EQUAL
    __id_filter_option: filter_option = filter_option.EQUAL

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value

    @property
    def name_filter_option(self) -> filter_option:
        return self.__name_filter_option

    @name_filter_option.setter
    def name_filter_option(self, value: filter_option):
        self.__name_filter_option = value

    @property
    def id_filter_option(self) -> filter_option:
        return self.__id_filter_option

    @id_filter_option.setter
    def id_filter_option(self, value: filter_option):
        self.__id_filter_option = value
