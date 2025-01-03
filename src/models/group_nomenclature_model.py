from src.core.base_models import base_model_name


class group_nomenclature_model(base_model_name):
    """Модель группы номенклатуры"""

    def __init__(self):
        super().__init__()

    def to_dict(self):
        return {
            "name": self.name,
            "unique_code": self.unique_code
        }

    @staticmethod
    def default_group_source():
        """Default группа - сырье (фабричный метод)"""
        item = group_nomenclature_model()
        item.name = "Сырье"
        return item

    @staticmethod
    def default_group_cold():
        """Default группа - заморозка (фабричный метод)"""
        item = group_nomenclature_model()
        item.name = "Заморозка"
        return item

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)

    # @staticmethod
    # def from_json(data):
    #     group_instance = group_nomenclature_model()
    #     group_instance.name = data.get('name', '')
    #     return group_instance

    def from_json(self, data):
        self.name = data.get('name', '')
        return self
