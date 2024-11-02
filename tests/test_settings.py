import json
import os
import tempfile
import unittest
from unittest.mock import patch, mock_open

from src.core.abstract_logic import abstract_logic
from src.core.custom_exception import argument_exception
from src.models.settings_model import settings
from src.settings_manager import settings_manager


class TestSettingsManager(unittest.TestCase):

    # for settings_manager.py
    @patch("builtins.open", new_callable=mock_open,
           read_data='{"organization_name": "TestNameOrg", "inn": "123456789101"}')
    def test_load_settings(self, mock_file):
        manager = settings_manager()
        result = manager.open("../settings.json")

        self.assertTrue(result)
        self.assertEqual(manager.current_settings.organization_name, "TestNameOrg")
        self.assertEqual(manager.current_settings.inn, "123456789101")

    def test_settings_manager_open_fail(self):
        manager1 = settings_manager()

        manager1.open("../settings58.json")

        print(manager1.error_text)
        self.assertTrue(manager1.is_error)

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file_path = os.path.join(self.test_dir.name, 'test_settings.json')

        self.test_data = {
            "organization_name": "Тестовая организация",
            "inn": "123456789012"
        }
        with open(self.test_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.test_data, f, ensure_ascii=False, indent=4)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_load_settings_from_file(self):
        manager = settings_manager()
        result = manager.open(self.test_file_path)

        self.assertTrue(result)
        self.assertEqual(manager.current_settings.organization_name, self.test_data['organization_name'])
        self.assertEqual(manager.current_settings.inn, self.test_data['inn'])

    def test_default_settings(self):
        manager = settings_manager()
        result = manager.open("nonexistent_settings.json")

        self.assertFalse(result)
        self.assertEqual(manager.current_settings.organization_name, "Рога и копыта (default)")
        self.assertEqual(manager.current_settings.inn, "380000000038")

    @patch("builtins.open", new_callable=mock_open,
           read_data='{"organization_name": "TestNameOrg", "inn": "123456789101"}')
    def test_singleton(self, mock_file):
        manager1 = settings_manager()
        manager1.open("../settings.json")

        manager2 = settings_manager()

        self.assertEqual(manager2.current_settings.inn, manager1.current_settings.inn)
        self.assertEqual(manager2.current_settings.organization_name, manager1.current_settings.organization_name)

        self.assertIs(manager1, manager2)

    # def test_settings_manager_singletone(self):
    #     # Подготовка
    #     manager1 = settings_manager()
    #     result = manager1.open("../settings.json")
    #
    #     # Действие
    #     manager2 = settings_manager()
    #
    #     # Проверки
    #     assert manager1.current_settings.inn == manager2.current_settings.inn
    #     assert manager1.current_settings.organization_name == manager2.current_settings.organization_name

    def test_open_invalid_type(self):
        # Передача некорректного типа в file_path
        manager = settings_manager()

        with self.assertRaises(argument_exception) as context:
            manager.open(123)

        self.assertTrue("Некорректный тип для параметра 'file_path'. Ожидается: str" in str(context.exception))

    def test_open_default_file_path(self):
        # Проверка установки пути по умолчанию
        manager = settings_manager()
        default_path = os.path.join(os.curdir, "../settings.json")
        result = manager.open("")

        self.assertIsInstance(result, bool)

    # for abstract_logic.py
    def test_error_text_setter(self):
        # Создаем подкласс, чтобы протестировать абстрактный класс
        class TestLogic(abstract_logic):
            def set_exception(self, ex: Exception):
                pass  # pragma: no cover

        test_instance = TestLogic()

        test_instance.error_text = "строка без пробелов"
        self.assertEqual(test_instance.error_text, "строка без пробелов")

        test_instance.error_text = "   строка с пробелами   "
        self.assertEqual(test_instance.error_text, "строка с пробелами")

        test_instance.error_text = ""
        self.assertEqual(test_instance.error_text, "")

    # for settings_model.py
    def test_organization_name_invalid_type(self):
        settings_instance = settings()
        # Проверяем, что передача некорректного типа вызывает кастомное исключение
        with self.assertRaises(argument_exception) as context:
            settings_instance.organization_name = 123  # Передаем некорректный тип, например, int

        # Проверяем, что сообщение об ошибке соответствует ожидаемому
        self.assertTrue("Некорректный тип для параметра 'organization_name'. Ожидается: str" in str(context.exception))

    def test_inn_invalid_type(self):
        settings_instance = settings()
        # передача некорректного типа для ИНН
        with self.assertRaises(argument_exception) as context:
            settings_instance.inn = 123456789012

        self.assertTrue("Некорректный тип для параметра 'inn'. Ожидается: str" in str(context.exception))

    def test_inn_invalid_length(self):
        settings_instance = settings()
        # передача строки некорректной длины для ИНН
        with self.assertRaises(argument_exception) as context:
            settings_instance.inn = "123456"

        self.assertTrue("Параметр 'inn' должен содержать 12 символов" in str(context.exception))

    def test_account_number_invalid_type(self):
        settings_instance = settings()
        with self.assertRaises(argument_exception) as context:
            settings_instance.account_number = 123456789012

        self.assertTrue("Некорректный тип для параметра 'account_number'. Ожидается: str" in str(context.exception))

    def test_account_number_invalid_length(self):
        settings_instance = settings()
        with self.assertRaises(argument_exception) as context:
            settings_instance.account_number = "1"

        self.assertTrue("Параметр 'account_number' должен содержать 11 символов" in str(context.exception))

    def test_correspondent_account_invalid_type(self):
        settings_instance = settings()
        with self.assertRaises(argument_exception) as context:
            settings_instance.correspondent_account = 123456789012

        self.assertTrue(
            "Некорректный тип для параметра 'correspondent_account'. Ожидается: str" in str(context.exception))

    def test_correspondent_account_invalid_length(self):
        settings_instance = settings()
        with self.assertRaises(argument_exception) as context:
            settings_instance.correspondent_account = "1"

        self.assertTrue("Параметр 'correspondent_account' должен содержать 11 символов" in str(context.exception))

    def test_bik_invalid_type(self):
        settings_instance = settings()
        with self.assertRaises(argument_exception) as context:
            settings_instance.bik = 123456789012

        self.assertTrue("Некорректный тип для параметра 'bik'. Ожидается: str" in str(context.exception))

    def test_bik_invalid_length(self):
        settings_instance = settings()
        with self.assertRaises(argument_exception) as context:
            settings_instance.bik = "1"

        self.assertTrue("Параметр 'bik' должен содержать 9 символов" in str(context.exception))

    def test_ownership_type_invalid_type(self):
        settings_instance = settings()
        with self.assertRaises(argument_exception) as context:
            settings_instance.ownership_type = 123456789012

        self.assertTrue("Некорректный тип для параметра 'ownership_type'. Ожидается: str" in str(context.exception))

    def test_ownership_type_invalid_length(self):
        settings_instance = settings()
        with self.assertRaises(argument_exception) as context:
            settings_instance.ownership_type = "1"

        self.assertTrue("Параметр 'ownership_type' должен содержать 5 символов" in str(context.exception))

    def test_correspondent_account_getter(self):
        # тест геттера
        settings_instance = settings()
        expected_value = "12345678901"
        settings_instance._settings__correspondent_account = expected_value

        self.assertEqual(settings_instance.correspondent_account, expected_value)

    def test_bik_getter(self):
        # тест геттера
        settings_instance = settings()
        expected_value = "123456789"
        settings_instance._settings__bik = expected_value

        self.assertEqual(settings_instance.bik, expected_value)

    def test_ownership_type_getter(self):
        # тест геттера
        settings_instance = settings()
        expected_value = "12345"
        settings_instance._settings__ownership_type = expected_value

        self.assertEqual(settings_instance.ownership_type, expected_value)

    def test_account_number_setter(self):
        settings_instance = settings()
        valid_value = "12345678901"
        settings_instance.account_number = valid_value
        self.assertEqual(settings_instance.account_number, valid_value)

    def test_correspondent_account_setter(self):
        settings_instance = settings()
        valid_value = "12345678901"
        settings_instance.correspondent_account = valid_value
        self.assertEqual(settings_instance.correspondent_account, valid_value)

    def test_bik_setter(self):
        settings_instance = settings()
        valid_value = "123456789"
        settings_instance.bik = valid_value
        self.assertEqual(settings_instance.bik, valid_value)

    def test_ownership_type_setter(self):
        settings_instance = settings()
        valid_value = "12345"
        settings_instance.ownership_type = valid_value
        self.assertEqual(settings_instance.ownership_type, valid_value)


class TestSavingSettingsManager(unittest.TestCase):

    def setUp(self):
        # Подготовка к тесту
        self.manager = settings_manager()
        self.file_path = os.path.join(os.curdir, "../settings.json")

    def test_save_settings(self):
        self.manager.current_settings.organization_name = "Тестовая организация"
        self.manager.current_settings.inn = "123456789012"
        self.manager.current_settings.account_number = "12345678901"
        self.manager.current_settings.correspondent_account = "10987654321"
        self.manager.current_settings.bik = "987654321"
        self.manager.current_settings.ownership_type = "ОООТЕ"
        self.manager.current_settings.report_settings = {"CSV": "csv_report",
                                                         "MARKDOWN": "markdown_report",
                                                         "JSON": "json_report",
                                                         "XML": "xml_report",
                                                         "RTF": "rtf_report"}
        self.manager.current_settings.default_format = 3
        self.manager.current_settings.block_period = "2024-10-01"

        # Сохраняем настройки
        self.manager.save_settings()

        self.assertTrue(os.path.exists(self.file_path), "Файл настроек не был создан.")

        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.assertEqual(data["organization_name"], "Тестовая организация")
            self.assertEqual(data["inn"], "123456789012")
            self.assertEqual(data["account_number"], "12345678901")
            self.assertEqual(data["correspondent_account"], "10987654321")
            self.assertEqual(data["bik"], "987654321")
            self.assertEqual(data["ownership_type"], "ОООТЕ")
            self.assertEqual(data["report_settings"], {"CSV": "csv_report",
                                                       "MARKDOWN": "markdown_report",
                                                       "JSON": "json_report",
                                                       "XML": "xml_report",
                                                       "RTF": "rtf_report"})
            self.assertEqual(data["default_format"], 3)
            self.assertEqual(data["block_period"], "2024-10-01")


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
