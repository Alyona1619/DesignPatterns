import unittest
import json
import os
import tempfile
from unittest.mock import patch, mock_open
from DesignPatterns.SettingsClasses.main import settings_manager

class TestSettingsManager(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open,
           read_data='{"organization_name": "TestNameOrg", "inn": "123456789101"}')
    def test_load_settings(self, mock_file):
        manager = settings_manager()
        result = manager.open("settings.json")

        self.assertTrue(result)
        self.assertEqual(manager.settings.organization_name, "TestNameOrg")
        self.assertEqual(manager.settings.inn, "123456789101")

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
        self.assertEqual(manager.settings.organization_name, self.test_data['organization_name'])
        self.assertEqual(manager.settings.inn, self.test_data['inn'])

    def test_default_settings(self):
        manager = settings_manager()
        result = manager.open("nonexistent_settings.json")

        self.assertFalse(result)
        self.assertEqual(manager.settings.organization_name, "Рога и копыта (default)")
        self.assertEqual(manager.settings.inn, "380000000038")

if __name__ == '__main__':
    unittest.main()

