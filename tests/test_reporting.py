from src.settings_manager import settings_manager
from src.start_service import start_service
from src.data_repository import data_repository
from src.reports.report_factory import report_factory
from src.core.format_reporting import format_reporting
from src.reports.csv_report import csv_report
from src.reports.markdown_report import markdown_report
from src.reports.json_report import json_report
from src.reports.xml_report import xml_report
from src.reports.rtf_report import rtf_report

import json
from src.deserializers.json_deserializer import JsonDeserializer
from src.models.ingredient import ingredient
from src.models.range_model import range_model


import unittest
import os

class test_reporting(unittest.TestCase):
    """Набор тестов для проверки работы формирование отчетов"""

    def setUp(self):
        """Подготовка тестовой среды перед каждым тестом"""
        self.manager = settings_manager()
        self.manager.open("../settings.json")
        self.repository = data_repository()
        self.start = start_service(self.repository, self.manager)
        self.start.create()

        os.makedirs("reports", exist_ok=True)

        self.reports_path = "./tests/reports"
        os.makedirs(self.reports_path, exist_ok=True)
        self.report_json = json_report()

    def test_csv_report_create_range(self):
        """Проверка работы отчета CSV"""
        report = csv_report()
        report.create(self.repository.data[data_repository.range_key()])
        assert report.result != ""

    def test_csv_report_create_nomenclature(self):
        """Проверка работы отчета CSV для номенклатуры"""
        report = csv_report()
        report.create(self.repository.data[data_repository.nomenclature_key()])
        assert report.result != ""

    def test_markdown_report_create_nomenclature(self):
        """Проверка работы отчета Markdown для номенклатуры"""
        report = markdown_report()
        report.create(self.repository.data[data_repository.nomenclature_key()])
        assert report.result != ""

    def test_json_report_create_nomenclature(self):
        """Проверка работы отчета JSON для номенклатуры"""
        report = json_report()
        report.create(self.repository.data[data_repository.nomenclature_key()])
        assert report.result != ""

    def test_xml_report_create_nomenclature(self):
        """Проверка работы отчета XML для номенклатуры"""
        report = xml_report()
        report.create(self.repository.data[data_repository.nomenclature_key()])
        assert report.result != ""

    def test_rtf_report_create_nomenclature(self):
        """Проверка работы отчета RTF для номенклатуры"""
        report = rtf_report()
        report.create(self.repository.data[data_repository.nomenclature_key()])
        assert report.result != ""

    def test_report_factory_create(self):
        """Проверить работу фабрики для получения инстанса нужного отчета"""
        factory = report_factory(self.manager)
        report = factory.create(format_reporting.CSV)
        assert report is not None
        assert isinstance(report, csv_report)

    def test_report_factory_create_fail(self):
        """Проверить работу фабрики. Не реализован формат"""
        factory = report_factory(self.manager)
        report = factory.create(format_reporting.TXT)
        assert report is None
        assert factory.is_error is True

    def test_csv_report_data_correctness(self):
        """Проверка корректности данных в отчете CSV"""
        report = csv_report()
        report.create(self.repository.data[data_repository.nomenclature_key()])
        lines = report.result.splitlines()
        assert len(lines) > 1  # есть заголовок и одна строка данных
        header = lines[0].split(";")
        assert header[0] == "full_name"  # Проверка, что первый заголовок - "name"
        data_row = lines[1].split(";")
        assert len(data_row) == len(header)  # Проверка, что данные соответствуют заголовкам

    def test_generate_reports(self):
        """Сгенерировать отчеты для единиц измерений в разных форматах"""
        # Generate CSV report
        csv_report_instance = csv_report()
        csv_report_instance.create(self.repository.data[data_repository.range_key()])
        with open("reports/range_report.csv", "w", encoding="utf-8") as f:
            f.write(csv_report_instance.result)

        # Generate Markdown report
        markdown_report_instance = markdown_report()
        markdown_report_instance.create(self.repository.data[data_repository.range_key()])
        with open("reports/range_report.md", "w", encoding="utf-8") as f:
            f.write(markdown_report_instance.result)

        # Generate JSON report
        json_report_instance = json_report()
        json_report_instance.create(self.repository.data[data_repository.range_key()])
        with open("reports/range_report.json", "w", encoding="utf-8") as f:
            f.write(json_report_instance.result)

        # Generate XML report
        xml_report_instance = xml_report()
        xml_report_instance.create(self.repository.data[data_repository.range_key()])
        with open("reports/range_report.xml", "w", encoding="utf-8") as f:
            f.write(xml_report_instance.result)

        # Generate RTF report
        rtf_report_instance = rtf_report()
        rtf_report_instance.create(self.repository.data[data_repository.range_key()])
        with open("reports/range_report.rtf", "w", encoding="utf-8") as f:
            f.write(rtf_report_instance.result)

    def test_generate_recipe_reports(self):
        """Сгенерировать отчеты для рецептов в разных форматах"""

        recipe = self.repository.data[data_repository.recipe_key()]
        recipe_data = recipe.ingredients

        csv_report_instance = csv_report()
        csv_report_instance.create(recipe_data)
        with open("reports/recipe_report.csv", "w", encoding="utf-8") as f:
            f.write(csv_report_instance.result)

        markdown_report_instance = markdown_report()
        markdown_report_instance.create(recipe_data)
        with open("reports/recipe_report.md", "w", encoding="utf-8") as f:
            f.write(markdown_report_instance.result)

        json_report_instance = json_report()
        json_report_instance.create(recipe_data)
        with open("reports/recipe_report.json", "w", encoding="utf-8") as f:
            f.write(json_report_instance.result)

        xml_report_instance = xml_report()
        xml_report_instance.create(recipe_data)
        with open("reports/recipe_report.xml", "w", encoding="utf-8") as f:
            f.write(xml_report_instance.result)

        rtf_report_instance = rtf_report()
        rtf_report_instance.create(recipe_data)
        with open("reports/recipe_report.rtf", "w", encoding="utf-8") as f:
            f.write(rtf_report_instance.result)

    def test_report_factory_create_default(self):
        """Проверить работу фабрики для создания отчета по умолчанию"""
        factory = report_factory(self.manager)
        report = factory.create_default()

        assert report is not None
        assert isinstance(report, json_report)

    def test_deserialize_json(self):
        """Проверка десериализации данных из JSON для recipe"""
        file_name = "reports/recipe_report.json"
        with open(file_name, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        des_recipe = JsonDeserializer.deserialize(json_data, 'recipe_model')

        stored_recipe = self.repository.data[data_repository.recipe_key()]

        print("des_recipe.ingredients", des_recipe.ingredients)
        print("stored_recipe.ingredients", stored_recipe.ingredients)

        self.assertEqual(len(des_recipe.ingredients), len(stored_recipe.ingredients),
                         "Количество ингредиентов должно совпадать")

        for deserialized_ingredient, stored_ingredient in zip(des_recipe.ingredients, stored_recipe.ingredients):
            self.assertEqual(deserialized_ingredient.nomenclature.full_name, stored_ingredient.nomenclature.full_name,
                             f"Ингредиенты должны совпадать: {deserialized_ingredient.nomenclature.full_name} != {stored_ingredient.nomenclature.full_name}")
            self.assertEqual(deserialized_ingredient.value, stored_ingredient.value,
                             f"Значения ингредиентов должны совпадать: {deserialized_ingredient.value} != {stored_ingredient.value}")

