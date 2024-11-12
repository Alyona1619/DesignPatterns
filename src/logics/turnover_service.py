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

    def get_osv(self, start_date: str, end_date: str, warehouse_id: str):
        """
        Получает оборот по складу за указанный период.

        :param start_date: Начальная дата периода (в формате 'YYYY-MM-DD')
        :param end_date: Конечная дата периода (в формате 'YYYY-MM-DD')
        :param warehouse_id: Идентификатор склада
        :return: Отфильтрованные данные по оборотам
        """
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        except operation_exception as e:
            raise operation_exception(f"Неверный формат даты. Используйте 'YYYY-MM-DD' {str(e)}")

        all_turnovers = self.__repository.data[data_repository.blocked_turnover_key()]

        filtered_turnovers = [
            turnover for turnover in all_turnovers
            if turnover.warehouse.id == warehouse_id and start_dt <= turnover.date <= end_dt
        ]

        init_balance = self.get_initial_balance(start_date, warehouse_id)

        osv_data = self.calculate_osv_report(filtered_turnovers, init_balance)

        return osv_data

    def get_initial_balance(self, start_date: str, warehouse_id: str):
        """
        Получаем начальное сальдо на склад по указанной дате.

        :param start_date: Начальная дата периода (в формате 'YYYY-MM-DD')
        :param warehouse_id: Идентификатор склада
        :return: Начальное сальдо
        """
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            # Логика для получения начального сальдо (например, за день до start_date)
            initial_balance_data = self.__repository.data[data_repository.blocked_turnover_key()]

            # Применение фильтра по складу и дате
            initial_balance = sum(turnover.turnover for turnover in initial_balance_data
                                  if turnover.warehouse.id == warehouse_id and turnover.date < start_dt)

            return initial_balance
        except Exception as e:
            raise operation_exception(f"Ошибка получения начального сальдо: {str(e)}")

    def calculate_osv_report(self, turnover_data, initial_balance):
        osv_report = []

        # Пример расчета оборотно-сальдовой ведомости
        for turnover in turnover_data:
            # Предполагаем, что turnover - это объект, содержащий количество (quantity) и другие поля
            current_balance = initial_balance + turnover.turnover  # или другой расчет сальдо

            osv_report.append({
                'nomenclature': turnover.nomenclature.name,
                'warehouse': turnover.warehouse.name,
                'turnover': turnover.turnover,
                'balance': current_balance,
            })

        return osv_report

    def update_turnover(self, data):
        turnovers = self.__repository.data.get(data_repository.blocked_turnover_key(), [])
        for turnover in turnovers:
            self.nomenclature_service.update_applied_nomenclature(turnover, data)

    def set_exception(self, ex: Exception):  # pragma: no cover
        super().set_exception(ex)

    def handle_event(self, type: event_type, params):
        if type == event_type.CHANGE_NOMENCLATURE_IN_TURNOVER:
            return self.update_turnover(params)
