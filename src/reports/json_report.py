import json
import uuid

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
            raise operation_exception("Empty data provided")
        report = []
        for row in data:
            report.append(self.serialize(row))
        self.result = json.dumps(report, ensure_ascii=False, indent=2)

    @staticmethod
    def serialize(data, visited=None) -> dict:
        if visited is None:
            visited = set()

            # Проверка, чтобы избежать повторной сериализации
        if id(data) in visited:
            return {}

        visited.add(id(data))

        row_data = {}
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(data.__class__, x)), dir(data)))
        for field in fields:
            value = getattr(data, field)

            # Обработка UUID
            if isinstance(value, uuid.UUID):
                row_data[field] = str(value)
            elif hasattr(value, '__dict__') and not isinstance(value, (str, int, float, bool)):
                row_data[field] = json_report.serialize(value, visited)
            elif isinstance(value, list):
                row_data[field] = []
                for val in value:
                    row_data[field].append(json_report.serialize(val, visited))
            else:
                row_data[field] = value
        return row_data

    # def create(self, data: list):
    #     validator.validate(data, list)
    #     if len(data) == 0:
    #         raise operation_exception("Набор данных пуст!")
    #
    #     result_data = []
    #     for row in data:
    #         row_dict = self.serialize_row(row)
    #         result_data.append(row_dict)
    #
    #     self.result = json.dumps(result_data, ensure_ascii=False, indent=4)
    #
    # def serialize_row(self, row):
    #     if hasattr(row, "__dict__"):
    #         return {k: v for k, v in row.__dict__.items() if not k.startswith("_") and not callable(v)}
    #     return {}


