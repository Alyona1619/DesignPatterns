from abc import ABC, abstractmethod


class Deserializer(ABC):
    """Абстрактный базовый класс для десериализаторов."""

    @abstractmethod
    def deserialize(self, data):
        pass
