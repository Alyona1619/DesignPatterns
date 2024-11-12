from src.core.abstract_logic import abstract_logic
from src.core.abstract_process import abstract_process
from src.core.event_type import event_type
from src.core.validator import argument_exception, validator


class process_factory(abstract_logic):
    _process_registry = {}

    @classmethod
    def register_process(cls, process_class):
        if not issubclass(process_class, abstract_process):
            raise argument_exception(f"Процесс {process_class.__name__} должен наследоваться от abstract_process")

        cls._process_registry[process_class.__name__] = process_class

    @classmethod
    def get_process(cls, process_name: str, *args, **kwargs) -> abstract_process:
        validator.validate(process_name, str)
        process_class = cls._process_registry.get(process_name)

        if process_class is None:
            raise argument_exception(f"Процесс с именем '{process_name}' не зарегистрирован в фабрике.")

        return process_class(*args, **kwargs)

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)
