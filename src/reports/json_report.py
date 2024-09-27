import json
from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.core.validator import validator, operation_exception


class json_report(abstract_report):
    """Ответ формирует набор данных в формате JSON"""

    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.JSON

    def create(self, data: list):
        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Набор данных пуст!")

        result_data = []
        for row in data:
            row_dict = self.serialize_row(row)
            result_data.append(row_dict)

        self.result = json.dumps(result_data, ensure_ascii=False, indent=4)

    def serialize_row(self, row):
        if hasattr(row, "__dict__"):
            return {k: v for k, v in row.__dict__.items() if not k.startswith("_") and not callable(v)}
        return {}


