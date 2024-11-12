import connexion
from flask import Response
from flask import request

from src.core.event_type import event_type
from src.core.format_reporting import format_reporting
from src.data_repository import data_repository
from src.deserializers.json_deserializer import JsonDeserializer
from src.logics.model_prototype import model_prototype
from src.logics.nomenclature_service import nomenclature_service
from src.logics.observe_service import observe_service
from src.logics.transaction_prototype import transaction_prototype
from src.processes.process_factory import process_factory
from src.processes.wh_blocked_turnover_process import warehouse_blocked_turnover_process
from src.processes.wh_turnover_process import warehouse_turnover_process
from src.reports.report_factory import report_factory
from src.settings_manager import settings_manager
from src.start_service import start_service

app = connexion.FlaskApp(__name__)

manager = settings_manager()
manager.open("settings.json")
repository = data_repository()
repository.data[data_repository.blocked_turnover_key()] = {}
service = start_service(repository, manager)
service.create()
rep_factory = report_factory(manager)
proc_factory = process_factory()

nomenclature_serv = nomenclature_service(repository)


@app.route("/api/reports/formats", methods=["GET"])
def formats():
    result = []
    for report in format_reporting:
        result.append({"name": report.name, "value": report.value})

    return result


@app.route("/api/reports/<category>/<format>", methods=["GET"])
def get_report(category, format):
    data_methods = [method for method in dir(data_repository) if
                    callable(getattr(data_repository, method)) and method.endswith('_key')]
    data = {method.replace('_key', ''): getattr(data_repository, method)() for method in data_methods}

    if category not in data:
        return Response(f"Указанная категория '{category}' отсутствует!", 400)

    try:
        report_format = format_reporting[format.upper()]
    except:
        return Response("Указанный формат отчёта отсутствует!", 400)

    try:
        report = rep_factory.create(report_format)
        report.create(repository.data[data[category]])
    except Exception as ex:
        return Response(f"Ошибка на сервере!", 500)

    return Response(report.result, 200)


@app.route("/api/filter/<category>", methods=["POST"])
def filter_data(category):
    data_methods = [method for method in dir(data_repository) if
                    callable(getattr(data_repository, method)) and method.endswith('_key')]
    categories = {method.replace('_key', ''): getattr(data_repository, method)() for method in data_methods}

    if category not in categories:
        return Response(f"Указанная категория '{category}' отсутствует!", 400)

    try:
        filter_data = request.get_json()

        filter_obj = JsonDeserializer.deserialize(filter_data, 'filter')

        prototype = model_prototype(repository.data[category]).create(repository.data[category], filter_obj)
        report = rep_factory.create_default()
        report.create(prototype.data)

        return report.result

    except Exception as ex:
        return Response(f"Ошибка на сервере: {str(ex)}", 500)


@app.route("/api/warehouse/transactions", methods=["POST"])
def get_warehouse_transactions():
    try:
        filter_data = request.get_json()

        filter_obj = JsonDeserializer.deserialize(filter_data, 'filter_transaction')

        t_data = repository.data[[data_repository.transaction_key()]]
        if not t_data:
            return Response("Нет данных", 400)

        prototype = transaction_prototype(t_data).create(t_data, filter_obj)

        report = rep_factory.create_default()
        report.create(prototype.data)

        return report.result

    except Exception as ex:
        return Response(f"Ошибка на сервере: {str(ex)}", 500)


@app.route("/api/warehouse/turnover", methods=["POST"])
def get_warehouse_turnover():
    try:
        filter_data = request.get_json()

        filter_obj = JsonDeserializer.deserialize(filter_data, 'filter_transaction')

        t_data = repository.data[[data_repository.transaction_key()]]
        if not t_data:
            return Response("Нет данных", 400)

        prototype = transaction_prototype(t_data).create(t_data, filter_obj)

        proc_factory.register_process(warehouse_turnover_process)
        process_class = proc_factory.get_process('warehouse_turnover_process', manager)

        turnovers = process_class.process(prototype.data)

        report = rep_factory.create_default()
        report.create(turnovers)

        return report.result

    except Exception as ex:
        return Response(f"Ошибка на сервере: {str(ex)}", 500)


@app.route('/api/settings/block_period', methods=['GET'])
def get_block_period():
    block_period = manager.get_block_period_str()
    return Response(f"block_period: {block_period}")


@app.route('/api/settings/new_block_period', methods=['POST'])
def set_block_period():
    try:
        data = request.get_json()
        new_block_period = data.get("block_period")

        if not new_block_period:
            return Response("Дата блокировки не указана!", status=400)

        manager.current_settings.block_period = new_block_period
        observe_service.raise_event(event_type.CHANGE_BLOCK_PERIOD, None)

        transactions = repository.data[data_repository.transaction_key()]
        if not transactions:
            return Response("Нет транзакций для пересчета.", status=400)

        proc_factory.register_process(warehouse_blocked_turnover_process)
        process_class = proc_factory.get_process('warehouse_blocked_turnover_process', manager)

        blocked_turnovers = process_class.process(transactions)
        repository.data[data_repository.blocked_turnover_key()] = blocked_turnovers

        return Response(f"Дата блокировки успешно обновлена. new_block_period: {new_block_period}."
                        f"Заблокированные обороты пересчитаны помещены в репозиторий данных: {len(blocked_turnovers)}",
                        status=200)

    except Exception as ex:
        return Response(f"Ошибка на сервере: {str(ex)}", status=500)


@app.route("/api/nomenclature/<id>", methods=["GET"])
def get_nomenclature(id):
    try:
        nomen = nomenclature_serv.get_nomenclature(id)

        report = rep_factory.create_default()
        report.create(nomen.data)

        return report.result

    except Exception as ex:
        return Response(f"Ошибка на сервере: {str(ex)}", status=500)


@app.route("/api/nomenclature", methods=["PUT"])
def add_nomenclature():
    try:
        data = request.get_json()

        new_nomenclature = nomenclature_serv.add_nomenclature(data)

        return Response(f"Номенклатура успешно добавлена: {new_nomenclature}", status=200)

    except Exception as ex:
        return Response(f"Ошибка на сервере: {str(ex)}", status=500)


@app.route("/api/nomenclature", methods=["PATCH"])
def update_nomenclature():
    try:
        data = request.get_json()

        observe_service.raise_event(event_type.CHANGE_NOMENCLATURE, data)

        return Response(f"Номенклатура успешно обновлена", status=200)

    except Exception as ex:
        return Response(f"Ошибка на сервере: {str(ex)}", status=500)


@app.route("/api/nomenclature", methods=["DELETE"])
def delete_nomenclature():
    try:
        data = request.get_json()

        observe_service.raise_event(event_type.DELETE_NOMENCLATURE, data)

        return Response(f"Номенклатура успешно удалена", status=200)

    except Exception as ex:
        return Response(f"Ошибка на сервере: {str(ex)}", status=500)


if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port=8080)
