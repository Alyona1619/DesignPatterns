from abc import ABC, abstractmethod


class abstract_process(ABC):

    @abstractmethod
    def process(self, transactions: list) -> list:
        pass
