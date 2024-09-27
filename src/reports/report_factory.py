from src.core.abstract_logic import abstract_logic
from src.core.abstract_report import abstract_report
from src.core.format_reporting import format_reporting
from src.reports.csv_report import csv_report
from src.reports.markdown_report import markdown_report
from src.reports.json_report import json_report
from src.reports.xml_report import xml_report
from src.reports.rtf_report import rtf_report
from src.core.validator import validator, operation_exception
from src.settings_manager import settings_manager


class report_factory(abstract_logic):
    """Фабрика для формирования отчетов"""
    __reports: dict

    def __init__(self, sttngmngr: settings_manager) -> None:
        super().__init__()
        # Наборы отчетов
        # self.__reports[format_reporting.CSV] = csv_report
        # self.__reports[format_reporting.MARKDOWN] = markdown_report
        # self.__reports[format_reporting.JSON] = json_report
        # self.__reports[format_reporting.XML] = xml_report
        # self.__reports[format_reporting.RTF] = rtf_report

        self.__reports = {
            format_reporting.CSV: csv_report,
            format_reporting.MARKDOWN: markdown_report,
            format_reporting.JSON: json_report,
            format_reporting.XML: xml_report,
            format_reporting.RTF: rtf_report
        }
        self.__sttngmngr = sttngmngr

    def create(self, format: format_reporting) -> abstract_report:
        """Получить инстанс нужного отчета"""
        validator.validate(format, format_reporting)

        if format not in self.__reports.keys():
            self.set_exception(operation_exception(f"Указанный вариант формата {format} не реализован!"))
            return None

        report = self.__reports[format]
        return report()

    def create_default(self) -> abstract_report:
        format = self.__settings_manager.current_settings.report_format
        return self.create(format)

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
