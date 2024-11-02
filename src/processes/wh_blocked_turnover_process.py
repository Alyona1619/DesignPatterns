from src.core.abstract_process import abstract_process
from src.core.transaction_type import transaction_type
from src.models.warehouse_turnover import warehouse_turnover_model
from src.settings_manager import settings_manager


class warehouse_blocked_turnover_process(abstract_process):

    def __init__(self, sttngmngr: settings_manager) -> None:
        self.sttngmngr = sttngmngr
        self.block_period = self.sttngmngr.current_settings.block_period

    def process(self, transactions: list):
        turnovers_data = {}

        for transaction in transactions:
            if transaction.period > self.block_period:
                continue

            key = (
                transaction.warehouse.unique_code, transaction.nomenclature.unique_code, transaction.range.unique_code)

            if key not in turnovers_data:
                turnovers_data[key] = warehouse_turnover_model.create(
                    warehouse=transaction.warehouse,
                    nomenclature=transaction.nomenclature,
                    range=transaction.range
                )

            if transaction.transaction_type == transaction_type.RECEIPT:
                turnovers_data[key].turnover += transaction.quantity
            elif transaction.transaction_type == transaction_type.EXPENDITURE:
                turnovers_data[key].turnover -= transaction.quantity

        return turnovers_data
