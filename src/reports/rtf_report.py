from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.core.validator import validator, operation_exception


class rtf_report(abstract_report):
    """Ответ формирует набор данных в формате RTF"""

    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.RTF

    def create(self, data: list):
        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Набор данных пуст!")

        # Начало RTF документа
        self.result = "{\\rtf1\\ansi\\ansicpg1251\\deff0\n"
        self.result += "{\\fonttbl{\\f0\\fnil\\fcharset0 Verdana;}}\n"
        self.result += "\\viewkind4\\uc1 \n"
        self.result += "\\pard\n"

        # Заголовок
        headers = [field for field in dir(data[0]) if
                   not field.startswith("_") and not callable(getattr(data[0], field))]
        header_line = "\\b " + " \\b0 \\pard\n".join(headers) + "\n"

        self.result += header_line

        # Данные
        for row in data:
            row_line = " ".join(f"{getattr(row, field)}" for field in headers)
            self.result += f"{row_line}\\par\n"

        # Конец RTF документа
        self.result += "}"
