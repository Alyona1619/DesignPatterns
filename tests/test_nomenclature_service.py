import unittest
from unittest.mock import patch, MagicMock
from src.data_repository import data_repository
from src.models.range_model import range_model
from src.settings_manager import settings_manager
from src.start_service import start_service
from src.logics.nomenclature_service import nomenclature_service
from src.models.nomenclature_model import nomenclature_model
from src.models.group_nomenclature_model import group_nomenclature_model
from src.core.validator import operation_exception


class TestNomenclatureService(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовой среды"""
        self.repository = data_repository()
        self.repository.data[data_repository.blocked_turnover_key()] = {}
        self.manager = settings_manager()
        self.service = start_service(self.repository, self.manager)
        self.service.create()
        self.nomenclature_service = nomenclature_service(self.repository)

    @patch('src.logics.nomenclature_service.model_prototype')
    def test_get_nomenclature_success(self, mock_prototype):
        """Тест успешного получения номенклатуры"""
        mock_data = [nomenclature_model.default_nomenclature("Test Nomenclature", "Group 1", "Unit 1")]
        mock_prototype.return_value.create.return_value = mock_data

        result = self.nomenclature_service.get_nomenclature("123")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].full_name, "Test Nomenclature")

    @patch('src.logics.nomenclature_service.model_prototype')
    def test_get_nomenclature_not_found(self, mock_prototype):
        """Тест, когда номенклатура не найдена"""
        mock_prototype.return_value.create.return_value = []

        with self.assertRaises(operation_exception):
            self.nomenclature_service.get_nomenclature("123")

    @patch('src.logics.nomenclature_service.model_prototype')
    def test_add_nomenclature_success(self, mock_prototype):
        """Тест успешного добавления номенклатуры"""
        data = {
            "full_name": "Тест",
            "group": {
                "name": "группа1",
                "unique_code": "424573c2-4db1-4e1f-a70c-55f43aa0b691"
            },
            "unit": {
                "base": None,
                "coef": 1,
                "name": "грамм1",
                "unique_code": "93fba799-4a3e-4050-b2ce-3a112078e668"
            }
        }

        mock_prototype_instance = MagicMock()
        mock_prototype_instance.create.return_value = MagicMock(data=[])
        mock_prototype.return_value = mock_prototype_instance

        new_nomenclature = self.nomenclature_service.add_nomenclature(data)

        self.assertEqual(new_nomenclature.full_name, "Тест")
        self.assertEqual(new_nomenclature.group.name, "группа1")
        self.assertEqual(new_nomenclature.unit.name, "грамм1")

    @patch('src.logics.nomenclature_service.model_prototype')
    def test_add_nomenclature_already_exists(self, mock_prototype):
        """Тест, когда номенклатура уже существует"""
        data = {
            "full_name": "Existing Nomenclature",
            "group": "Group 1",
            "unit": "Unit 1"
        }

        # Патчируем model_prototype, чтобы вернуть существующую номенклатуру
        mock_prototype.return_value.create.return_value = [nomenclature_model.default_nomenclature("Existing Nomenclature", "Group 1", "Unit 1")]

        with self.assertRaises(operation_exception):
            self.nomenclature_service.add_nomenclature(data)

    @patch('src.logics.nomenclature_service.model_prototype')
    def test_update_nomenclature_not_found(self, mock_prototype):
        """Тест, когда номенклатура не найдена для обновления"""
        data = {"unique_code": "123", "full_name": "Updated Nomenclature"}

        mock_prototype.return_value.create.return_value = []

        with self.assertRaises(operation_exception):
            self.nomenclature_service.update_nomenclature(data)

    @patch('src.logics.nomenclature_service.model_prototype')
    def test_delete_nomenclature_success(self, mock_prototype):
        """Тест успешного удаления номенклатуры"""
        data = {"unique_code": self.repository.data[data_repository.nomenclature_key()][0].unique_code}

        mock_prototype.return_value.create.return_value = [nomenclature_model.default_nomenclature("Test Nomenclature", "Group 1", "Unit 1")]

        self.nomenclature_service.delete_nomenclature(data)

        self.assertEqual(len(self.repository.data[data_repository.nomenclature_key()]), 0)

    @patch('src.logics.nomenclature_service.model_prototype')
    def test_delete_nomenclature_not_found(self, mock_prototype):
        """Тест, когда номенклатура не найдена для удаления"""
        data = {"unique_code": "123"}

        mock_prototype.return_value.create.return_value = []

        with self.assertRaises(operation_exception):
            self.nomenclature_service.delete_nomenclature(data)


if __name__ == '__main__':
    unittest.main()

