from src.core.abstract_process import abstract_process
from src.core.validator import argument_exception, validator
from src.processes.wh_turnover_process import warehouse_turnover_process


class ProcessFactory:
    _process_registry = {}

    @classmethod
    def register_process(cls, process_class):
        if not issubclass(process_class, abstract_process):
            raise argument_exception(f"Процесс {process_class.__name__} должен наследоваться от abstract_process")

        cls._process_registry[process_class.__name__] = process_class

    @classmethod
    def create_process(cls, process_name: str) -> abstract_process:
        validator.validate(process_name, str)
        process_class = cls._process_registry.get(process_name)

        if process_class is None:
            raise argument_exception(f"Процесс с именем '{process_name}' не зарегистрирован в фабрике.")

        return process_class()


