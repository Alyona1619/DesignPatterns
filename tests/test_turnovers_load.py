import time
import unittest

from src.data_repository import data_repository
from src.processes.wh_blocked_turnover_process import warehouse_blocked_turnover_process
from src.settings_manager import settings_manager
from src.start_service import start_service


class LoadTestTurnoversBlockPeriod(unittest.TestCase):

    def setUp(self):
        self.reposity = data_repository()
        self.reposity.data[data_repository.blocked_turnover_key()] = {}
        self.manager = settings_manager()
        self.service = start_service(self.reposity, self.manager)
        self.service.create()

        self.warehouse = self.reposity.data[data_repository.warehouse_key()][0]
        self.nomenclature = self.reposity.data[data_repository.nomenclature_key()][0]
        self.range = self.reposity.data[data_repository.range_key()][0]
        self.transactions = self.reposity.data[data_repository.transaction_key()]

    def test_load_turnover_with_diff_block_dates(self):
        block_dates = [
            "2024-01-01",
            # datetime(2024, 1, 1),
            "2024-03-01",
            "2024-06-01",
            "2024-09-01",
            "2024-12-01"
        ]
        print("\n")
        for block_date in block_dates:
            self.manager.current_settings.block_period = block_date
            blocked_turnover_process = warehouse_blocked_turnover_process(self.manager)

            start_time = time.time()
            result = blocked_turnover_process.process(self.transactions)
            end_time = time.time()

            elapsed_time = end_time - start_time

            print(f"Дата блокировки: {block_date}, Время выполнения: {elapsed_time:.4f} секунд")
            self.assertIsNotNone(result, "Результат расчета не должен быть None")
