from src.core.abstract_logic import abstract_logic
from src.core.event_type import event_type
from src.data_repository import data_repository
from src.logics.nomenclature_service import nomenclature_service
from src.logics.observe_service import observe_service


class recipe_service(abstract_logic):
    def __init__(self, repository: data_repository):
        observe_service.append(self)
        self.__repository = repository
        self.nomenclature_service = nomenclature_service(repository)

    def update_recipe(self, data):
        recipes = self.__repository.data.get(data_repository.recipe_key(), [])
        for recipe in recipes:
            self.nomenclature_service.update_applied_nomenclature(recipe, data)

    def set_exception(self, ex: Exception):  # pragma: no cover
        super().set_exception(ex)

    def handle_event(self, type: event_type, params):
        if type == event_type.CHANGE_NOMENCLATURE_IN_RECIPE:
            self.update_recipe(params)
