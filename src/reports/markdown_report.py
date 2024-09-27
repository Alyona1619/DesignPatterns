from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.core.validator import validator, operation_exception


class markdown_report(abstract_report):
    """Ответ формирует набор данных в формате Markdown"""

    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.MARKDOWN

    def create(self, data: list):
        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Набор данных пуст!")

        first_model = data[0]

        # Список полей от типа назначения
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)),
                             dir(first_model)))

        # Заголовок
        for field in fields:
            self.result += f"**{str(field)}**  | "

        self.result += "\n"

        # Данные
        for row in data:
            for field in fields:
                value = getattr(row, field)
                self.result += f"{str(value)}  | "
            self.result += "\n"
