from datetime import datetime

from src.core.abstract_logic import abstract_logic
from src.core.event_type import event_type
from src.core.validator import operation_exception
from src.data_repository import data_repository
from src.logics.nomenclature_service import nomenclature_service
from src.logics.observe_service import observe_service


class turnover_service(abstract_logic):
    def __init__(self, repository: data_repository):
        observe_service.append(self)
        self.__repository = repository
        self.nomenclature_service = nomenclature_service(repository)

    def update_turnover(self, data):
        turnovers = self.__repository.data.get(data_repository.blocked_turnover_key(), [])
        for turnover in turnovers:
            self.nomenclature_service.update_applied_nomenclature(turnover, data)

    def set_exception(self, ex: Exception):  # pragma: no cover
        super().set_exception(ex)

    def handle_event(self, type: event_type, params):
        if type == event_type.CHANGE_NOMENCLATURE_IN_TURNOVER:
            return self.update_turnover(params)
