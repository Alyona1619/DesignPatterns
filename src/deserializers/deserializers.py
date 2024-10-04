from src.deserializers.deserialize_factory import DeserializerFactory
from src.models.group_nomenclature_model import group_nomenclature_model
from src.models.ingredient import ingredient
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.deserializers.abstract_deserializer import Deserializer

class NomenclatureDeserializer(Deserializer):
    def deserialize(self, data):
        nomenclature_instance = nomenclature_model()
        nomenclature_instance.full_name = data.get('full_name', '')
        nomenclature_instance.group = DeserializerFactory.get_deserializer('group').deserialize(data['group'])
        nomenclature_instance.unit = DeserializerFactory.get_deserializer('range').deserialize(data['unit'])
        return nomenclature_instance

class GroupDeserializer(Deserializer):
    def deserialize(self, data):
        group_instance = group_nomenclature_model()
        group_instance.name = data.get('name', '')
        return group_instance

class RangeDeserializer(Deserializer):
    def deserialize(self, data):
        range_instance = range_model()
        range_instance.name = data.get('name', '')
        range_instance.coef = data.get('coef', 1)
        range_instance.base = None
        return range_instance

class IngredientDeserializer(Deserializer):
    def deserialize(self, data):
        ingredient_instance = ingredient()
        ingredient_instance.value = data.get('value', 0)
        ingredient_instance.nomenclature = DeserializerFactory.get_deserializer('nomenclature').deserialize(data['nomenclature'])
        return ingredient_instance

#from src.deserializers.abstract_deserializer import Deserializer
# from src.deserializers.deserialize_factory import DeserializeFactory
# from src.models.group_nomenclature_model import group_nomenclature_model
# from src.models.ingredient import ingredient
# from src.models.nomenclature_model import nomenclature_model
# from src.models.range_model import range_model
#
#
# class NomenclatureDeserializer(Deserializer):
#
#     _maps = {
#         nomenclature_model: 'Nomenclature',
#         group_nomenclature_model: 'Group',
#         range_model: 'Range',
#         ingredient: 'Ingredient',
#     }
#
#     def deserialize(self, data):
#         nomenclature_instance = nomenclature_model()
#         nomenclature_instance.full_name = data.get('full_name', '')
#         nomenclature_instance.group = DeserializeFactory.get_deserializer('group').deserialize(data['group'])
#         nomenclature_instance.unit = DeserializeFactory.get_deserializer('range').deserialize(data['unit'])
#         return nomenclature_instance
#
#
# class GroupDeserializer(Deserializer):
#
#     def deserialize(self, data):
#         group_instance = group_nomenclature_model()
#         group_instance.name = data.get('name', '')
#         return group_instance
#
#
# class RangeDeserializer(Deserializer):
#
#     def deserialize(self, data):
#         range_instance = range_model()
#         range_instance.name = data.get('name', '')
#         return range_instance
#
#
# class IngredientDeserializer(Deserializer):
#
#     def deserialize(self, data):
#         ingredient_instance = ingredient()
#         ingredient_instance.name = data.get('name', '')
#         ingredient_instance.quantity = data.get('quantity', 0)
#         return ingredient_instance

