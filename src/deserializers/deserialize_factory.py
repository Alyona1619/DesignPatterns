from src.core.abstract_reference import abstract_reference
from src.core.validator import argument_exception


class DeserializeFactory:
    @staticmethod
    def get_deserializer(data_type):
        subclasses = abstract_reference.__subclasses__()
        deserializer_map = {
            cls.__name__.lower(): cls for cls in subclasses
        }

        if data_type in deserializer_map:
            return deserializer_map[data_type]
        else:
            raise argument_exception(f"Неизвестный тип данных для десериализации: {data_type}")



