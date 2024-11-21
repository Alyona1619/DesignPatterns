import json
import unittest

from src.core.validator import operation_exception
from src.data_repository import data_repository
from src.models.warehouse_turnover import warehouse_turnover_model
from src.reports.tbs_report import tbs_report
from src.repository_manager import repository_manager
from src.settings_manager import settings_manager
from src.start_service import start_service


class TestTBSReport(unittest.TestCase):
    """Тесты для формирования TBS отчета"""

    def setUp(self):
        """Подготовка данных перед тестами"""
        self.repository = data_repository()
        self.manager = settings_manager()
        self.manager.open("../settings.json")
        self.rep_manager = repository_manager(self.repository, self.manager)
        self.service = start_service(self.repository, self.manager, self.rep_manager)
        self.service.create()

        self.warehouse_1 = self.repository.data[data_repository.warehouse_key()][0]

        self.nomenclature_1 = self.repository.data[data_repository.nomenclature_key()][0]
        self.nomenclature_2 = self.repository.data[data_repository.nomenclature_key()][1]

        self.range_1 = self.repository.data[data_repository.range_key()][0]
        self.range_2 = self.repository.data[data_repository.range_key()][1]

    def test_tbs_report_empty_data(self):
        """Проверка на пустые данные"""
        report = tbs_report()

        # Попытка создать отчет с пустыми данными
        with self.assertRaises(operation_exception):
            report.create([])

    def test_tbs_report_with_valid_data(self):
        """Проверка корректности данных в отчете TBS"""
        report = tbs_report()

        # Данные для формирования отчета
        turnover_data_before = [
            warehouse_turnover_model.create(warehouse=self.warehouse_1,
                                            nomenclature=self.nomenclature_1,
                                            range=self.range_1,
                                            turnover=25.0),
            warehouse_turnover_model.create(warehouse=self.warehouse_1,
                                            nomenclature=self.nomenclature_2,
                                            range=self.range_1,
                                            turnover=100.0)
        ]
        turnover_data_between = [
            warehouse_turnover_model.create(warehouse=self.warehouse_1,
                                            nomenclature=self.nomenclature_1,
                                            range=self.range_1,
                                            turnover=240.0),
            warehouse_turnover_model.create(warehouse=self.warehouse_1,
                                            nomenclature=self.nomenclature_2,
                                            range=self.range_1,
                                            turnover=22.0)
        ]

        data = [turnover_data_before, turnover_data_between]

        # Генерация отчета
        report.create(data)

        self.assertTrue(len(report.result) > 0)

        report_json = json.loads(report.result)
        for entry in report_json:
            self.assertIn("warehouse", entry)
            self.assertIn("nomenclature", entry)
            self.assertIn("start_balance", entry)
            self.assertIn("turnover_for_period", entry)
            self.assertIn("end_balance", entry)
            self.assertEqual(entry["end_balance"], entry["start_balance"] + entry["turnover_for_period"])

            if entry["nomenclature"] == self.nomenclature_1.name:
                expected_start_balance = 25.0
                expected_turnover_for_period = 240.0
                expected_end_balance = expected_start_balance + expected_turnover_for_period
            elif entry["nomenclature"] == self.nomenclature_2.name:
                expected_start_balance = 100.0
                expected_turnover_for_period = 22.0
                expected_end_balance = expected_start_balance + expected_turnover_for_period
            else:
                continue

            self.assertEqual(entry["start_balance"], expected_start_balance)
            self.assertEqual(entry["turnover_for_period"], expected_turnover_for_period)
            self.assertEqual(entry["end_balance"], expected_end_balance)


if __name__ == '__main__':
    unittest.main()
