import unittest

from src.core.custom_exception import argument_exception
from src.models.range_model import range_model
from src.settings_manager import settings_manager
from src.models.organization_model import organization_model


class test_models(unittest.TestCase):

    # the most important tests
    def test_org_model_loaded_from_settings(self):
        manager = settings_manager()
        manager.open("../settings.json")

        company = organization_model()
        company.from_settings(manager.current_settings)

        self.assertEqual(company.inn, manager.current_settings.inn)  # pragma: no cover
        self.assertEqual(company.bik, manager.current_settings.bik)  # pragma: no cover
        self.assertEqual(company.account_number, manager.current_settings.account_number)  # pragma: no cover
        self.assertEqual(company.ownership_type, manager.current_settings.ownership_type)  # pragma: no cover

    def test_range_model_creation(self):
        gram = range_model()
        gram.name = "грамм"
        gram.base_unit = None
        gram.conversion_factor = 1.0

        self.assertEqual(gram.name, "грамм")
        self.assertIsNone(gram.base_unit)
        self.assertEqual(gram.conversion_factor, 1.0)

        kilogram = range_model()
        kilogram.name = "килограмм"
        kilogram.base_unit = gram
        kilogram.conversion_factor = 1000.0

        self.assertEqual(kilogram.name, "килограмм")
        self.assertEqual(kilogram.base_unit, gram)
        self.assertEqual(kilogram.conversion_factor, 1000.0)

    def test_comparison_diff(self):
        base_range = range_model()
        base_range.name = "грамм"

        new_range = range_model()
        new_range.name = "килограмм"

        self.assertNotEqual(base_range, new_range)

    def test_comparison_sim(self):
        base_range = range_model()
        base_range.name = "грамм"

        new_range = range_model()
        new_range.name = "грамм"

        self.assertEqual(base_range, new_range)

    def test_range_conversion(self):
        base_range = range_model()
        base_range.name = "грамм"

        new_range = range_model()
        new_range.name = "килограмм"
        new_range.coef = 1000
        new_range.base = base_range

        convert = new_range.to_base

        self.assertEqual(convert.name, 'грамм')
        self.assertEqual(convert.base, None)

    # other tests for range_model
    def test_base_setter_invalid_type(self):
        range_instance = range_model()
        with self.assertRaises(argument_exception) as context:
            range_instance.base = "invalid_type"
        self.assertTrue(
            "Некорректный тип для параметра 'base'. Ожидается: range_model or None" in str(context.exception))

    def test_coef_setter_invalid_type(self):
        range_instance = range_model()
        with self.assertRaises(argument_exception) as context:
            range_instance.coef = 0
        self.assertTrue(
            "Параметр 'coef' должен содержать positive number символов" in str(context.exception))

    def test_to_base_method_none(self):
        range_instance = range_model()
        # когда base == None
        result = range_instance.to_base
        self.assertEqual(result, range_instance)

    def test_set_compare_mode(self):
        unit1 = range_model()
        unit1.name = "Unit1"
        unit2 = range_model()
        unit2.name = "Unit2"

        # с none
        result = unit1.set_compare_mode(None)
        self.assertFalse(result)
        # с объектом другого типа
        result = unit1.set_compare_mode("Not a range_model")
        self.assertFalse(result)
        # с другим объектом range_model
        result = unit1.set_compare_mode(unit2)
        self.assertFalse(result)

    # test for organization_model.py
    def test_inn_property(self):
        obj = organization_model()
        test_inn = "380000000038"
        obj.inn = test_inn
        self.assertEqual(obj.inn, test_inn)

    def test_bik_property(self):
        obj = organization_model()
        test_bik = "044525225"
        obj.bik = test_bik
        self.assertEqual(obj.bik, test_bik)

    def test_account_number_property(self):
        obj = organization_model()
        test_account_number = "12345678901"
        obj.account_number = test_account_number
        self.assertEqual(obj.account_number, test_account_number)

    def test_ownership_form_property(self):
        obj = organization_model()
        test_ownership_type = "12345"
        obj.ownership_type = test_ownership_type
        self.assertEqual(obj.ownership_type, test_ownership_type)

    def test_inn_invalid_type(self):
        obj = organization_model()
        # передача некорректного типа для ИНН
        with self.assertRaises(argument_exception) as context:
            obj.inn = 123456789012

        self.assertTrue("Некорректный тип для параметра 'inn'. Ожидается: str" in str(context.exception))

    def test_inn_invalid_length(self):
        obj = organization_model()
        # передача строки некорректной длины для ИНН
        with self.assertRaises(argument_exception) as context:
            obj.inn = "123456"

        self.assertTrue("Параметр 'inn' должен содержать 12 символов" in str(context.exception))

    def test_account_number_invalid_type(self):
        obj = organization_model()
        with self.assertRaises(argument_exception) as context:
            obj.account_number = 123456789012

        self.assertTrue("Некорректный тип для параметра 'account_number'. Ожидается: str" in str(context.exception))

    def test_account_number_invalid_length(self):
        obj = organization_model()
        with self.assertRaises(argument_exception) as context:
            obj.account_number = "1"

        self.assertTrue("Параметр 'account_number' должен содержать 11 символов" in str(context.exception))

    def test_bik_invalid_type(self):
        obj = organization_model()
        with self.assertRaises(argument_exception) as context:
            obj.bik = 123456789012

        self.assertTrue("Некорректный тип для параметра 'bik'. Ожидается: str" in str(context.exception))

    def test_bik_invalid_length(self):
        obj = organization_model()
        with self.assertRaises(argument_exception) as context:
            obj.bik = "1"

        self.assertTrue("Параметр 'bik' должен содержать 9 символов" in str(context.exception))

    def test_ownership_type_invalid_type(self):
        obj = organization_model()
        with self.assertRaises(argument_exception) as context:
            obj.ownership_type = 123456789012

        self.assertTrue("Некорректный тип для параметра 'ownership_type'. Ожидается: str" in str(context.exception))

    def test_ownership_type_invalid_length(self):
        obj = organization_model()
        with self.assertRaises(argument_exception) as context:
            obj.ownership_type = "1"

        self.assertTrue("Параметр 'ownership_type' должен содержать 5 символов" in str(context.exception))
