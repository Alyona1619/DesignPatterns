import json

from src.core.abstract_report import abstract_report
from src.core.format_reporting import format_reporting
from src.core.validator import validator, operation_exception


class tbs_report(abstract_report):
    """Ответ формирует набор данных в формате JSON"""

    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.TBS

    def create(self, data: list):
        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Empty data provided")

        turnover_data_before = data[0]
        turnover_data_between = data[1]

        report = []
        for turnover_before, turnover_between in zip(turnover_data_before, turnover_data_between):
            report_entry = {
                "warehouse": turnover_before.warehouse.name,
                "nomenclature": turnover_before.nomenclature.full_name,
                "range": turnover_before.range.name,
                "start_balance": turnover_before.turnover,
                "turnover_for_period": turnover_between.turnover,
                "end_balance": turnover_before.turnover + turnover_between.turnover
            }
            report.append(report_entry)

        self.result = json.dumps(report, ensure_ascii=False, indent=2)
