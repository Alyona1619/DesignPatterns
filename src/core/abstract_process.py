from abc import ABC, abstractmethod


class abstract_process(ABC):
    """Абстрактный класс для наследования процессов"""

    @abstractmethod
    def process(self, transactions: list) -> list:
        pass
