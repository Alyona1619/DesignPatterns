from src.deserializers.deserialize_factory import DeserializeFactory


class JsonDeserializer:
    @staticmethod
    def deserialize(json_data, data_type):
        model_class = DeserializeFactory.get_deserializer(data_type)

        instance = model_class()

        if isinstance(json_data, list):
            for item in json_data:
                instance.from_json(item)
        elif isinstance(json_data, dict):  # Обработка одиночного объекта
            instance.from_json(json_data)
        else:
            raise ValueError("json_data должен быть списком или объектом")
        return instance
