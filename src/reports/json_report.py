import json
import uuid
from datetime import datetime
from enum import Enum

from src.core.abstract_report import abstract_report
from src.core.format_reporting import format_reporting
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

        if id(data) in visited:
            return {}

        visited.add(id(data))

        row_data = {}
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(data.__class__, x)), dir(data)))

        for field in fields:
            value = getattr(data, field)

            # if field == "to_base":
            #     continue
            if isinstance(value, property):
                continue
            # Обработка UUID
            if isinstance(value, uuid.UUID):
                row_data[field] = str(value)
            elif isinstance(value, Enum):
                row_data[field] = value.value
            elif isinstance(value, datetime):
                row_data[field] = value.strftime('%Y-%m-%d')
            elif hasattr(value, '__dict__') and not isinstance(value, (str, int, float, bool)):
                row_data[field] = json_report.serialize(value, visited)
            elif isinstance(value, list):
                row_data[field] = []
                for val in value:
                    row_data[field].append(json_report.serialize(val, visited))
                    print("+++")
            else:
                row_data[field] = value
        return row_data
