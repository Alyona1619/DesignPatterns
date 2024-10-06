from src.core.abstract_reference import abstract_reference
from src.models.nomenclature_model import nomenclature_model


class ingredient(abstract_reference):
    __nomenclature: nomenclature_model = None
    __value: float = 0

    @property
    def nomenclature(self):
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value):
        self.__nomenclature = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)

    @staticmethod
    def default_ingredient(nomenclature: nomenclature_model, quantity: int):
        ing = ingredient()
        ing.nomenclature = nomenclature
        ing.value = quantity
        return ing

    # @staticmethod
    # def from_json(data):
    #     """Фабричный метод для десериализации ингредиента из JSON."""
    #     ingredient_instance = ingredient()
    #     ingredient_instance.value = data.get('value', 0)
    #     ingredient_instance.nomenclature = nomenclature_model.from_json(data['nomenclature'])
    #     return ingredient_instance

    def from_json(self, data):
        """Метод для десериализации ингредиента из JSON."""
        try:
            self.value = data.get('value', 0)
            self.nomenclature = nomenclature_model().from_json(data['nomenclature'])
            print("Вытащили nomenclature:", self.nomenclature.full_name)
            return self
        except KeyError as e:
            print(f"Ошибка десериализации: отсутствует ключ {e}")
            raise
