from src.core.abstract_reference import abstract_reference
from src.models.ingredient_model import ingredient_model
from src.models.step_model import step_model

class recipe_model(abstract_reference):
    __name: str = ""
    __servings: int = 0
    __prep_time: str = ""
    __ingredients: list[ingredient_model] = []
    __steps: list[step_model] = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        if len(value) > 255:
            # TODO переделать исключения
            raise ValueError("Название рецепта должно содержать не более 255 символов")
        self.__name = value

    @property
    def servings(self):
        return self.__servings

    @servings.setter
    def servings(self, value: int):
        if value <= 0:
            # TODO переделать исключения
            raise ValueError("Количество порций должно быть положительным числом")
        self.__servings = value

    @property
    def prep_time(self):
        return self.__prep_time

    @prep_time.setter
    def prep_time(self, value: str):
        self.__prep_time = value

    @property
    def ingredients(self):
        return self.__ingredients

    @ingredients.setter
    def ingredients(self, value: list[ingredient_model]):
        self.__ingredients = value

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, value: list[step_model]):
        self.__steps = value
