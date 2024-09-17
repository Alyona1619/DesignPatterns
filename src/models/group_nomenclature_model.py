from src.core.base_models import base_model_name

"""
Модель группы номенклатуры
"""


class group_nomenclature_model(base_model_name):

    """
    Default группа - сырье (фабричный метод)
    """
    @staticmethod
    def default_group_source():
        item = group_nomenclature_model()
        item.name = "Сырье"
        return item

    """
    Default группа - заморозка (фабричный метод)
    """
    @staticmethod
    def default_group_cold():
        item = group_nomenclature_model()
        item.name = "Заморозка"
        return item

# from src.core.abstract_reference import abstract_reference
#
#
# class group_nomenclature_model(abstract_reference):
#     def __init__(self):
#         super().__init__()
#
#     def set_compare_mode(self, other_object) -> bool:
#         super().set_compare_mode(other_object)
