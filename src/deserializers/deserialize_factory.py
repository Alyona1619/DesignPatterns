from src.deserializers.deserializers import NomenclatureDeserializer, GroupDeserializer, RangeDeserializer, IngredientDeserializer
from src.core.validator import argument_exception

class DeserializerFactory:
    """Фабрика для создания десериализаторов различных моделей"""
    @staticmethod
    def get_deserializer(data_type):
        if data_type == 'nomenclature':
            return NomenclatureDeserializer()
        elif data_type == 'group':
            return GroupDeserializer()
        elif data_type == 'range':
            return RangeDeserializer()
        elif data_type == 'ingredient':
            return IngredientDeserializer()
        else:
            raise argument_exception(f"Неизвестный тип данных для десериализации: {data_type}")
