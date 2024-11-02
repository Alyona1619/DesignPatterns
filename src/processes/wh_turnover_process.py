from datetime import datetime

from src.core.abstract_process import abstract_process
from src.core.transaction_type import transaction_type
from src.models.warehouse_transaction import warehouse_transaction_model
from src.models.warehouse_turnover import warehouse_turnover_model
from src.settings_manager import settings_manager


class warehouse_turnover_process(abstract_process):

    def __init__(self, sttngmngr: settings_manager = None, blocked_turnovers: dict = {}):
        self.block_period = sttngmngr.get_block_period_date() if sttngmngr else datetime.now()
        self.blocked_turnovers = blocked_turnovers

    def process(self, transactions: list[warehouse_transaction_model]) -> list[warehouse_turnover_model]:
        turnovers_data = {}

        for transaction in transactions:
            if transaction.period >= self.block_period:
                key = (transaction.warehouse.unique_code,
                       transaction.nomenclature.unique_code,
                       transaction.range.unique_code)

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

        for key, turnover in self.blocked_turnovers.items():
            if key in turnovers_data:
                turnovers_data[key].turnover += turnover.turnover
            else:
                turnovers_data[key] = turnover

        turnover_list = list(turnovers_data.values())
        return turnover_list
