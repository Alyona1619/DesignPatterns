import unittest

from src.core.event_type import event_type
from src.core.validator import operation_exception
from src.data_repository import data_repository
from src.logics.nomenclature_service import nomenclature_service
from src.logics.observe_service import observe_service
from src.models.group_nomenclature_model import group_nomenclature_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.settings_manager import settings_manager
from src.start_service import start_service


class TestNomenclatureService(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовой среды"""
        self.repository = data_repository()
        self.repository.data[data_repository.blocked_turnover_key()] = {}
        self.manager = settings_manager()
        self.service = start_service(self.repository, self.manager)
        self.service.create()
        self.nomenclature_service = nomenclature_service(self.repository)

    def test_get_nomenclature_success(self):
        """Тест успешного получения номенклатуры"""
        id = self.repository.data[data_repository.nomenclature_key()][0].unique_code

        result = self.nomenclature_service.get_nomenclature(id)

        self.assertEqual(result.data[0].full_name, "Мука пшеничная")

    def test_get_nomenclature_not_found(self):
        """Тест, когда номенклатура не найдена"""
        id = "424573c2-4db1-4e1f-a70c-55f43aa0b691"

        with self.assertRaises(operation_exception):
            self.nomenclature_service.get_nomenclature(id)

    def test_add_nomenclature_success(self):
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

        # Добавляем номенклатуру
        new_nomenclature = self.nomenclature_service.add_nomenclature(data)

        self.assertEqual(new_nomenclature.full_name, "Тест")
        self.assertEqual(new_nomenclature.group.name, "группа1")
        self.assertEqual(new_nomenclature.unit.name, "грамм1")

    def test_add_nomenclature_already_exists(self):
        """Тест, когда номенклатура уже существует"""
        existing_nomenclature = nomenclature_model.default_nomenclature("Existing Nomenclature", "Group 1", "Unit 1")
        self.repository.data[data_repository.nomenclature_key()] = [existing_nomenclature]

        data = {
            "full_name": "Existing Nomenclature",
            "group": "Group 1",
            "unit": "Unit 1"
        }

        with self.assertRaises(operation_exception):
            self.nomenclature_service.add_nomenclature(data)

    def test_update_nomenclature_with_event(self):
        nomen = {
            "full_name": "Мук",
            "group": {
                "unique_code": self.repository.data[data_repository.group_nomenclature_key()][1].unique_code,
                "name": "Сырье"
            },
            "unique_code": self.repository.data[data_repository.nomenclature_key()][0].unique_code,
            "name": "",
            "range": {
                "base_range": None,
                "conversion_factor": 1,
                "unique_code": self.repository.data[data_repository.range_key()][0].unique_code,
                "name": "гр"
            }
        }

        observe_service.raise_event(event_type.CHANGE_NOMENCLATURE, nomen)

        assert self.repository.data[data_repository.nomenclature_key()][0].full_name == "Мук"
        assert self.repository.data[data_repository.recipe_key()][0].ingredients[0].nomenclature.full_name == "Мук"
        assert self.repository.data[data_repository.blocked_turnover_key()][0].nomenclature.full_name == "Мук"

    def test_update_nomenclature_not_found(self):
        """Тест, когда номенклатура не найдена для обновления"""
        data = {"unique_code": "123", "full_name": "Updated Nomenclature"}

        self.repository.data[data_repository.nomenclature_key()] = []

        with self.assertRaises(operation_exception):
            self.nomenclature_service.update_nomenclature(data)

    def test_add_and_delete_nomenclature(self):
        """Тест, который сначала добавляет, а затем удаляет номенклатуру"""
        nomen = nomenclature_model.default_nomenclature("Что-то",
                                                        group_nomenclature_model.default_group_source(),
                                                        range_model.default_range_gramm())

        self.repository.data[data_repository.nomenclature_key()].append(nomen)

        data_for_deletion = {"unique_code": nomen.unique_code}
        self.nomenclature_service.delete_nomenclature(data_for_deletion)

        self.assertEqual(len(self.repository.data[data_repository.nomenclature_key()]), 2)

    def test_add_and_delete_nomenclature_with_event(self):
        """Тест, который сначала добавляет, а затем удаляет номенклатуру с использованием события"""
        nomen = nomenclature_model.default_nomenclature("Что-то",
                                                        group_nomenclature_model.default_group_source(),
                                                        range_model.default_range_gramm())

        self.repository.data[data_repository.nomenclature_key()].append(nomen)

        data_for_deletion = {"unique_code": nomen.unique_code}

        observe_service.raise_event(event_type.DELETE_NOMENCLATURE, data_for_deletion)

        self.assertEqual(len(self.repository.data[data_repository.nomenclature_key()]), 2)

    def test_delete_nomenclature_not_found(self):
        """Тест, когда номенклатура не найдена для удаления"""
        data = {"unique_code": "123"}

        self.repository.data[data_repository.nomenclature_key()] = []

        with self.assertRaises(operation_exception):
            self.nomenclature_service.delete_nomenclature(data)

    def test_delete_nomenclature_which_is_in_recipe_and_turnovers(self):
        """Тест удаления номенклатуры, которая используется в рецептах и оборотах"""
        existing_nomenclature = self.repository.data[data_repository.nomenclature_key()][0]

        data_for_deletion = {"unique_code": existing_nomenclature.unique_code}

        self.nomenclature_service.delete_nomenclature(data_for_deletion)

        with self.assertRaises(operation_exception):
            self.nomenclature_service.delete_nomenclature(data_for_deletion)


if __name__ == '__main__':
    unittest.main()
