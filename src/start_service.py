from src.core.abstract_logic import abstract_logic
from src.data_repository import data_repository
from src.core.validator import validator
from src.models.group_nomenclature_model import group_nomenclature_model
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.recipe_model import recipe_model
from src.models.ingredient import ingredient
from src.settings_manager import settings_manager
from src.models.settings_model import settings


class start_service(abstract_logic):
    """Сервис для реализации первого старта приложения"""
    __repository: data_repository = None
    __settings_manager: settings_manager = None

    def __init__(self, repository: data_repository, manager: settings_manager) -> None:
        super().__init__()
        validator.validate(repository, data_repository)
        validator.validate(manager, settings_manager)
        self.__repository = repository
        self.__settings_manager = manager

    @property
    def settings(self) -> settings:
        """Текущие настройки"""
        return self.__settings_manager.current_settings

    def __create_nomenclature_groups(self):
        """Сформировать группы номенклатуры"""
        nglist = []
        nglist.append(group_nomenclature_model.default_group_cold())
        nglist.append(group_nomenclature_model.default_group_source())
        self.__repository.data[data_repository.group_key()] = nglist

    def __create_nomenclature(self):
        """Сформировать номенклатуру"""
        group_source = group_nomenclature_model.default_group_source()
        range = range_model.default_range_gramm()
        nomenclature_list = [nomenclature_model.default_nomenclature("Мука пшеничная", group_source, range),
                             nomenclature_model.default_nomenclature("Сахар", group_source, range)]
        self.__repository.data[data_repository.nomenclature_key()] = nomenclature_list

    def __create_range(self):
        """Сформировать единицы измерения"""
        range_list = [range_model.default_range_gramm(), range_model.default_range_piece()]
        self.__repository.data[data_repository.range_key()] = range_list

    def __create_ingredients(self, ingredients_config):
        """Создать список ингредиентов"""
        nomenclature_group = group_nomenclature_model.default_group_source()
        return [self.__create_ingredient(ing, nomenclature_group, ing["range"]) for ing in ingredients_config] # брать еще range из ngredient config


    def __create_ingredient(self, ing, nomenclature_group, range):
        """Cоздание одного ингредиента"""
        nomenclature = nomenclature_model.default_nomenclature(ing["full_name"], nomenclature_group, range)
        elem = ingredient.default_ingredient(nomenclature, ing["value"])
        return elem

    # def __create_ingredient(self, ing, nomenclature_group):
    #     """Cоздание одного ингредиента"""
    #     nomenclature = nomenclature_model.default_nomenclature(ing["full_name"], nomenclature_group)
    #     elem = ingredient.default_ingredient(nomenclature, ing["value"])
    #     return elem

    def __create_recipe(self):
        """Cоздание рецепта"""
        recipe = recipe_model()

        ings = [
            {"name": "Пшеничная мука", "full_name": "Пшеничная мука", "value": 100,
             "range": range_model.default_range_gramm()},
            {"name": "Сахар", "full_name": "Сахар", "value": 80, "range": range_model.default_range_gramm()},
            {"name": "Сливочное масло", "full_name": "Сливочное масло", "value": 70,
             "range": range_model.default_range_gramm()},
            {"name": "Яйца", "full_name": "Яйца", "value": 1, "range": range_model.default_range_piece()},
            {"name": "Ванилин", "full_name": "Ванилин", "value": 5, "range": range_model.default_range_gramm()}
        ]

        recipe.ingredients = self.__create_ingredients(ings)
        recipe.name = 'ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ'
        recipe.step = '''1. Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты. Из данного 
        количества у меня получилось 8 штук диаметром около 10 см. 2. Масло положите в сотейник с толстым дном. 
        Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке. 3. Добавьте в теплое масло 
        сахар. Перемешайте венчиком до полного растворения сахара. От тепла сахар довольно быстро растает. 4. 
        Добавьте в масло яйцо. Предварительно все-таки проверьте масло, не горячее ли оно, иначе яйцо может 
        свариться. Перемешайте яйцо с маслом до однородности. 5. Всыпьте муку, добавьте ванилин. 6. Перемешайте массу 
        венчиком до состояния гладкого однородного теста. 7. Разогрейте вафельницу по инструкции к ней. У меня очень 
        старая, еще советских времен электровафельница. Она может и не очень красивая, но печет замечательно! Я не 
        смазываю вафельницу маслом, в тесте достаточно жира, да и к ней уже давно ничего не прилипает. Но вы смотрите 
        по своей модели. Выкладывайте тесто по столовой ложке. Можно класть немного меньше теста, тогда вафли будут 
        меньше и их получится больше. 9. Пеките вафли несколько минут до золотистого цвета. Осторожно откройте 
        вафельницу, она очень горячая! Снимите вафлю лопаткой. Горячая она очень мягкая, как блинчик. '''

        self.__repository.data[data_repository.recipe_key()] = recipe

    def create(self) -> bool:
        """Первый старт"""
        try:
            self.__create_nomenclature_groups()
            self.__create_range()
            self.__create_nomenclature()
            self.__create_recipe()
            return True
        except Exception as ex:
            self.set_exception(ex)
            return False

    def set_exception(self, ex: Exception):
        """Перегрузка абстрактного метода"""
        self._inner_set_exception(ex)
