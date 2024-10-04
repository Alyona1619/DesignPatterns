from src.core.abstract_reference import abstract_reference
from src.core.custom_exception import argument_exception


class range_model(abstract_reference):
    """Модель единицы измерения"""
    __base_unit = None
    __conversion_coeff = 1.0

    def __init__(self):
        super().__init__()

    @property
    def base(self):
        """Базовая единица измерения"""
        return self.__base_unit

    @base.setter
    def base(self, value):
        if value is not None and not isinstance(value, range_model):
            argument_exception.raise_type_error("base", "range_model or None")
        self.__base_unit = value

    @property
    def coef(self):
        """Коэффициент пересчета"""
        return self.__conversion_coeff

    @coef.setter
    def coef(self, value):
        if value <= 0:
            argument_exception.raise_value_error("coef", "positive number")
        self.__conversion_coeff = value

    def to_base(self):
        """Метод для преобразования в базовую единицу измерения"""
        if self.base is None:
            return self
        return self.base
        # base_unit = self.base
        # conversion_factor = self.coef
        # while base_unit.base is not None:
        #     base_unit = base_unit.base
        #     conversion_factor *= base_unit.coef
        # base_unit.coef = conversion_factor
        # return base_unit

    @staticmethod
    def default_range_gramm():
        item = range_model()
        item.name = "грамм"
        item.base = None
        item.coef = 1
        return item

    @staticmethod
    def default_range_piece():
        item = range_model()
        item.name = "штука"
        item.base = None
        item.coef = 1
        return item

    def set_compare_mode(self, other_object) -> bool:
        """Режим сравнения (по наименованию)"""
        if other_object is None:
            return False
        if not isinstance(other_object, range_model):
            return False

        return self.name == other_object.name

    @staticmethod
    def from_json(data):
        range_instance = range_model()
        range_instance.name = data.get('name', '')
        range_instance.coef = data.get('coef', 1)
        return range_instance

    # def from_json(self, data):
    #     self.name = data.get('name', '')
    #     self.coef = data.get('coef', 1)
    #     return self
