from src.core.abstract_reference import abstract_reference
from src.models.ingredient import ingredient


class recipe_model(abstract_reference):
    __name: str
    __ingredients: list[ingredient]
    __step: str

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def ingredients(self):
        return self.__ingredients

    @ingredients.setter
    def ingredients(self, value):
        self.__ingredients = value

    @property
    def step(self):
        return self.__step

    @step.setter
    def step(self, value):
        self.__step = value

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)

    # def from_json(self, data):
    #     """Метод для десериализации рецепта из JSON."""
    #     self.name = data.get('name', '')
    #
    #     self.ingredients = []
    #
    #     if isinstance(data, dict):
    #         ing = ingredient().from_json(data)
    #         self.ingredients.append(ing)
    #     # print(":", [ing.value for ing in self.ingredients])
    #     self.step = data.get('step', '')
    #     return self

    def from_json(self, data):
        """Метод для десериализации рецепта или списка ингредиентов из JSON."""
        # Проверка, является ли data списком
        if isinstance(data, list):
            # Обнуляем список ингредиентов перед заполнением
            self.ingredients = []
            for item in data:
                ing = ingredient().from_json(item)
                self.ingredients.append(ing)
        elif isinstance(data, dict):
            self.name = data.get('name', '')
            # Обнуляем список ингредиентов перед заполнением
            self.ingredients = []
            # Создаем ингредиент из текущего объекта
            ing = ingredient().from_json(data)
            self.ingredients.append(ing)

        self.step = data.get('step', '')
        return self

    # def from_json(self, data):
    #     """Метод для десериализации рецепта и его ингредиентов из JSON."""
    #     self.name = data.get('name', '')
    #
    #     # Обнуляем список ингредиентов перед заполнением
    #     self.ingredients = []
    #
    #     if isinstance(data, list):
    #         # Обрабатываем список ингредиентов
    #         for item in data:
    #             ing = ingredient().from_json(item)
    #             self.ingredients.append(ing)
    #     elif isinstance(data, dict):
    #         # Обрабатываем один ингредиент, если это словарь
    #         ing = ingredient().from_json(data)
    #         self.ingredients.append(ing)
    #
    #     self.step = data.get('step', '')
    #     return self

    # def from_json(self, data):
    #     self.name = data.get('name', '')
    #     print("Пришла data:", data)
    #     self.ingredients = [ingredient().from_json(ing) for ing in data.get('ingredients', [])]
    #     print("Вытащили ingredients1:", self.ingredients)
    #     print("Вытащили ingredients2:", [ing.value for ing in self.ingredients])
    #     self.step = data.get('step', '')
    #     return self


