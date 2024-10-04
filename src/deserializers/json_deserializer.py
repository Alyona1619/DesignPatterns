from src.deserializers.deserialize_factory import DeserializeFactory


class JsonDeserializer:
    @staticmethod
    def deserialize(json_data, data_type):
        factory = DeserializeFactory.get_deserializer(data_type)
        if isinstance(json_data, list):
            return [factory.from_json(item) for item in json_data]
        else:
            return factory.from_json(json_data)


# from src.models.ingredient import ingredient
#
#
# class JsonDeserializer:
#
#     @staticmethod
#     def deserialize_recipe(json_data):
#         recipe_list = []
#         for item in json_data:
#             ingredient_instance = ingredient.from_json(item)
#             recipe_list.append(ingredient_instance)
#         return recipe_list



# from src.deserializers.deserialize_factory import DeserializeFactory
#
#
# class JsonDeserializer:
#     @staticmethod
#     def deserialize(json_data, data_type):
#         factory = DeserializeFactory.get_deserializer(data_type)
#         return factory.from_json(json_data)
#
#     @staticmethod
#     def deserialize_recipe(json_data):
#         return [JsonDeserializer.deserialize(item, 'ingredient') for item in json_data]