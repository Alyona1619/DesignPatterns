import json
import unittest
import os
from src.data_repository import data_repository
from src.settings_manager import settings_manager
from src.repository_manager import repository_manager
from src.start_service import start_service


class TestRepositoryManager(unittest.TestCase):
    """Тесты для методов save_data и load_data"""

    def setUp(self):
        """Подготовка данных перед тестами"""
        self.repository = data_repository()
        self.manager = settings_manager()
        self.manager.open("../settings.json")
        self.rep_manager = repository_manager(self.repository, self.manager)
        self.service = start_service(self.repository, self.manager, self.rep_manager)
        self.service.create()

    def test_save_data_creates_file_and_is_not_empty(self):
        """Тестируем метод save_data: создание файла и его непустое содержимое"""

        self.rep_manager.save_data()

        file_path = "data_repository.json"
        self.assertTrue(os.path.exists(file_path), "Файл data_repository.json не был создан.")

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            self.assertGreater(len(content), 0, "Файл data_repository.json пуст.")
            data = json.loads(content)

            # Проверяем первое значение в файле
            group_nomenclature = data.get("group_nomenclature", [])
            self.assertGreater(len(group_nomenclature), 0, "Массив 'group_nomenclature' пуст.")
            first_item = group_nomenclature[0]

            # Проверяем соответствие первого элемента
            self.assertEqual(first_item["name"], "Заморозка",
                             "Неверное имя для первого элемента в 'group_nomenclature'.")

        os.remove(file_path)

    def test_load_data_restores_data(self):
        """Тестируем метод load_data: восстановление данных из файла"""

        # Сохраняем данные
        self.rep_manager.save_data()

        # Запоминаем какое-то значение из репозитория, например, первый элемент в group_nomenclature
        original_value = self.repository.data[data_repository.group_nomenclature_key()][0]

        # Вызовем метод load_data для восстановления данных
        self.rep_manager.load_data()

        # Проверим, что данные были восстановлены корректно, сравнив значения
        restored_value = self.repository.data[data_repository.group_nomenclature_key()][0]

        # Сравниваем старое и новое значение
        self.assertEqual(original_value.name, restored_value.name, "Имя восстановленного элемента не совпадает.")

        os.remove("data_repository.json")


if __name__ == '__main__':
    unittest.main()