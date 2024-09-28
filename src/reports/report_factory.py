from src.core.abstract_logic import abstract_logic
from src.core.abstract_report import abstract_report
from src.core.format_reporting import format_reporting
from src.core.validator import validator, argument_exception
from src.settings_manager import settings_manager



class report_factory(abstract_logic):
    """Фабрика для формирования отчетов"""
    __reports: dict = {}

    def __init__(self, sttngmngr: settings_manager) -> None:
        super().__init__()
        self.__reports = sttngmngr.current_settings.report_settings

    def create(self, format: format_reporting) -> abstract_report:
        validator.validate(format, format_reporting)

        if self.__reports is None:
            self.set_exception(argument_exception("Настройки отчетов не были загружены."))
            return None

        format_str = format.name
        if format_str not in self.__reports.keys():
            self.set_exception(argument_exception(f"Указанный вариант формата '{format}' не реализован!"))
            return None

        report_class_name = self.__reports[format_str]
        report_class = getattr(__import__(f'src.reports.{report_class_name}', fromlist=[report_class_name]),
                               report_class_name)

        return report_class()

    def default_create(self):
        if self.__reports is None:
            self.set_exception(argument_exception("Настройки отчетов не были загружены."))
            return None

        default_format_str = list(self.__reports.keys())[0] if self.__reports else None
        if default_format_str is None:
            self.set_exception(argument_exception("Нет формат отчета по умолчанию"))
            return None

        report_class_name = self.__reports[default_format_str]
        report_class = getattr(__import__(f'src.reports.{report_class_name}', fromlist=[report_class_name]),
                               report_class_name)

        return report_class()

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)


