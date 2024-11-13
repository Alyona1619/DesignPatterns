from src.core.abstract_logic import abstract_logic
from src.core.abstract_report import abstract_report
from src.core.event_type import event_type
from src.core.format_reporting import format_reporting
from src.core.validator import validator, argument_exception
from src.models.settings_model import settings
from src.settings_manager import settings_manager


class report_factory(abstract_logic):
    """Фабрика для формирования отчетов"""
    __reports: dict = {}
    __settings: settings = None

    def __init__(self, sttngmngr: settings_manager) -> None:
        super().__init__()
        self.__reports = sttngmngr.current_settings.report_settings
        self.__settings = sttngmngr.current_settings

    def create(self, format: format_reporting) -> abstract_report:
        validator.validate(format, format_reporting)

        if not isinstance(format, format_reporting):
            raise argument_exception(
                f"Неверный формат отчета: {format}. Ожидается один из: {', '.join([f.name for f in format_reporting])}")

        if self.__reports is None:
            self.set_exception(argument_exception("Настройки отчетов не были загружены."))
            return None

        format_str = format.name
        print("format ", format)
        print("format_str ", format_str)
        if format_str not in self.__reports.keys():
            self.set_exception(argument_exception(f"Указанный вариант формата '{format}' не реализован!"))
            return None

        report_class_name = self.__reports[format_str]
        report_class = getattr(__import__(f'src.reports.{report_class_name}', fromlist=[report_class_name]),
                               report_class_name)
        return report_class()

    def create_default(self) -> abstract_report:
        format = self.__settings.default_format
        return self.create(format)

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)
