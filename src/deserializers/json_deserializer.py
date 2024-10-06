from src.deserializers.deserialize_factory import DeserializeFactory


class JsonDeserializer:
    @staticmethod
    def deserialize(json_data, data_type):
        model_class = DeserializeFactory.get_deserializer(data_type)

        instance = model_class()

        if isinstance(json_data, list):
            for item in json_data:
                instance.from_json(item)

            return instance
        else:
            raise ValueError("json_data должен быть списком")





# class JsonDeserializer:
#     @staticmethod
#     def deserialize(json_data, data_type):
#         factory = DeserializeFactory.get_deserializer(data_type)
#         if isinstance(json_data, list):
#             print("factory.from_json(json_data)", [factory.from_json(item) for item in json_data])
#             return [factory.from_json(item) for item in json_data]
#         else:
#             print("factory.from_json(json_data)", factory.from_json(json_data))
#             return factory.from_json(json_data)
