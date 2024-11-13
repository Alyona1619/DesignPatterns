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

    def from_json(self, data):
        """Метод для десериализации ингредиента из JSON."""
        try:
            print("data from ingredient.py ", data)
            self.value = data.get('value', 0)
            self.nomenclature = nomenclature_model().from_json(data['nomenclature'])
            return self
            # ingredients_data = data.get('ingredients', [])
            # ingredients = []
            #
            # for ingredient_data in ingredients_data:
            #     ingredient_item = ingredient()
            #
            #     # Получаем данные о номенклатуре и десериализуем с помощью from_json
            #     nomenclature_data = ingredient_data.get('nomenclature', {})
            #     print("nomenclature_data ", nomenclature_data)
            #     ingredient_item.nomenclature = nomenclature_model().from_json(nomenclature_data)
            #
            #     # Устанавливаем значение (quantity) для ингредиента
            #     ingredient_item.value = ingredient_data.get('value', 0)
            #
            #     # Добавляем в список ингредиентов
            #     ingredients.append(ingredient_item)
            #
            # return ingredients
        except KeyError as e:
            print(f"Ошибка десериализации: отсутствует ключ {e}")
            raise

    # @staticmethod
    # def from_json(data):
    #     """Фабричный метод для десериализации ингредиента из JSON."""
    #     ingredient_instance = ingredient()
    #     ingredient_instance.value = data.get('value', 0)
    #     ingredient_instance.nomenclature = nomenclature_model.from_json(data['nomenclature'])
    #     return ingredient_instance
