from src.models.ingredient import ingredient

class JsonDeserializer:
    """Класс для десериализации рецептов из JSON через фабричные методы моделей."""

    @staticmethod
    def deserialize_recipe(json_data):
        recipe_list = []
        for item in json_data:
            ingredient_instance = ingredient.from_json(item)
            recipe_list.append(ingredient_instance)
        return recipe_list
