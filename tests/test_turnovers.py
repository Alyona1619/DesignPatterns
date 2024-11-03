import unittest
from datetime import datetime

from src.core.transaction_type import transaction_type
from src.data_repository import data_repository
from src.models.warehouse_transaction import warehouse_transaction_model
from src.processes.wh_turnover_process import warehouse_turnover_process
from src.settings_manager import settings_manager
from src.start_service import start_service


class TestWarehouseTurnover(unittest.TestCase):

    def setUp(self):
        self.reposity = data_repository()
        self.manager = settings_manager()
        self.service = start_service(self.reposity, self.manager)
        self.service.create()

        if len(self.reposity.data[data_repository.nomenclature_key()]) == 0:
            raise Exception("Нет данных!")

        self.warehouse_1 = self.reposity.data[data_repository.warehouse_key()][0]
        self.warehouse_2 = self.reposity.data[data_repository.warehouse_key()][1]

        self.nomenclature_1 = self.reposity.data[data_repository.nomenclature_key()][0]
        self.nomenclature_2 = self.reposity.data[data_repository.nomenclature_key()][1]

        self.range_1 = self.reposity.data[data_repository.range_key()][0]
        self.range_2 = self.reposity.data[data_repository.range_key()][1]

        self.transactions = [
            # для склада 1
            warehouse_transaction_model.create(period=datetime(2024, 10, 23, 12, 12, 0),
                                               warehouse=self.warehouse_1,
                                               nomenclature=self.nomenclature_1,
                                               range=self.range_1,
                                               quantity=100,
                                               transaction_type=transaction_type.RECEIPT),
            warehouse_transaction_model.create(period=datetime(2024, 10, 23, 12, 55, 0),
                                               warehouse=self.warehouse_1,
                                               nomenclature=self.nomenclature_1,
                                               range=self.range_1,
                                               quantity=50,
                                               transaction_type=transaction_type.EXPENDITURE),
            warehouse_transaction_model.create(period=datetime(2024, 10, 23, 15, 0, 0),
                                               warehouse=self.warehouse_1,
                                               nomenclature=self.nomenclature_1,
                                               range=self.range_1,
                                               quantity=25,
                                               transaction_type=transaction_type.EXPENDITURE),

            # для склада 2
            warehouse_transaction_model.create(period=datetime(2024, 10, 23),
                                               warehouse=self.warehouse_2,
                                               nomenclature=self.nomenclature_2,
                                               range=self.range_2,
                                               quantity=200,
                                               transaction_type=transaction_type.RECEIPT),
            warehouse_transaction_model.create(period=datetime(2024, 10, 24),
                                               warehouse=self.warehouse_2,
                                               nomenclature=self.nomenclature_2,
                                               range=self.range_2,
                                               quantity=100,
                                               transaction_type=transaction_type.EXPENDITURE),
        ]

        self.turnover_process = warehouse_turnover_process()

    def test_turnover_calculation_warehouse_1(self):
        turnover_results = self.turnover_process.process(self.transactions[:3])

        expected_turnover = 100 - 50 - 25  # 100 (поступление) - 50 (выдача) - 25 (выдача)
        actual_turnover = turnover_results[0].turnover

        self.assertEqual(actual_turnover, expected_turnover, "Оборот для склада 1 рассчитан неверно.")

    def test_turnover_calculation_warehouse_2(self):
        turnover_results = self.turnover_process.process(self.transactions[3:])

        expected_turnover = 200 - 100  # 200 (поступление) - 100 (выдача)
        actual_turnover = turnover_results[0].turnover

        self.assertEqual(actual_turnover, expected_turnover, "Оборот для склада 2 рассчитан неверно.")

    def test_block_period_change_does_not_affect_turnover_calculation(self):
        original_block_period = self.manager.get_block_period_str()
        new_block_period = "2024-03-15"

        self.manager.current_settings.block_period = new_block_period

        # Рассчитаем оборот с новой датой блокировки
        turnover_results_with_new_block = self.turnover_process.process(self.transactions)

        # Восстановим оригинальную дату блокировки
        self.manager.current_settings.block_period = original_block_period

        # Рассчитаем оборот с оригинальной датой блокировки
        turnover_results_with_original_block = self.turnover_process.process(self.transactions)

        self.assertEqual(turnover_results_with_new_block, turnover_results_with_original_block,
                         "Изменение даты блокировки повлияло на расчет оборота.")


if __name__ == '__main__':
    unittest.main()
