from DesignPatterns.src.abstract_reference import abstract_reference
from DesignPatterns.src.custom_exception import argument_exception

"""
Модель единицы измерения
"""
class range_model(abstract_reference):
    __base_unit = None
    __conversion_coeff = 1.0

    """
    Базовая единица измерения
    """
    @property
    def base(self):
        return self.__base_unit

    @base.setter
    def base(self, value):
        if value is not None and not isinstance(value, range_model):
            argument_exception.raise_type_error("base", "range_model or None")
        self.__base_unit = value

    """
    Коэффициент пересчета
    """
    @property
    def coef(self):
        return self.__conversion_coeff

    @coef.setter
    def coef(self, value):
        if value <= 0:
            argument_exception.raise_value_error("coef", "positive number")
        self.__conversion_coeff = value

    """
    Метод для преобразования в базовую единицу измерения
    """
    @property
    def to_base(self):
        if self.base is None:
            return self
        base_unit = self.base
        conversion_factor = self.coef
        while base_unit.base is not None:
            base_unit = base_unit.base
            conversion_factor *= base_unit.coef
        base_unit.coef = conversion_factor
        return base_unit

    """
    Режим сравнения (по наименованию)
    """
    def set_compare_mode(self, other_object) -> bool:
        if other_object is None:
            return False
        if not isinstance(other_object, range_model):
            return False

        return self.name == other_object.name

