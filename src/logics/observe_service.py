from src.core.abstract_logic import abstract_logic
from src.core.event_type import event_type
from src.core.validator import argument_exception


class observe_service:
    observers = []

    @staticmethod
    def append(service: abstract_logic):

        if service is None:
            return

        if not isinstance(service, abstract_logic):
            raise argument_exception("Некорректный тип данных!")

        items = list(map(lambda x: type(x).__name__, observe_service.observers))
        found = type(service).__name__ in items
        if not found:
            observe_service.observers.append(service)

    @staticmethod
    def raise_event(type: event_type, params):
        for instance in observe_service.observers:
            if instance is not None:
                instance.handle_event(type, params)
