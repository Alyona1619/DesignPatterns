from src.core.transaction_type import transaction_type
from src.models.warehouse_transaction import warehouse_transaction_model
from src.models.warehouse_turnover import warehouse_turnover_model
from src.core.abstract_process import abstract_process


class warehouse_turnover_process(abstract_process):

    def process(self, transactions: list[warehouse_transaction_model]) -> list[warehouse_turnover_model]:
        turnover_data = {}

        for transaction in transactions:
            key = (transaction.warehouse.unique_code,
                   transaction.nomenclature.unique_code,
                   transaction.range.unique_code)

            if key not in turnover_data:
                turnover_data[key] = warehouse_turnover_model.create(
                    warehouse=transaction.warehouse,
                    nomenclature=transaction.nomenclature,
                    range=transaction.range
                )

            if transaction.transaction_type == transaction_type.RECEIPT:
                turnover_data[key].turnover += transaction.quantity
            elif transaction.transaction_type == transaction_type.EXPENDITURE:
                turnover_data[key].turnover -= transaction.quantity

        turnover_list = list(turnover_data.values())
        return turnover_list
