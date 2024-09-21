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

