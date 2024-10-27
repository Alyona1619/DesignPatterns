from enum import Enum


class transaction_type(Enum):
    """Типы транзакций"""
    RECEIPT = "RECEIPT"
    EXPENDITURE = "EXPENDITURE"
