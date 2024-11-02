from datetime import datetime

import connexion
from flask import Response
from src.core.format_reporting import format_reporting
from src.data_repository import data_repository
from src.logics.model_prototype import model_prototype
from src.logics.transaction_prototype import transaction_prototype
from src.processes.wh_turnover_process import warehouse_turnover_process
from src.settings_manager import settings_manager
from src.start_service import start_service
from src.reports.report_factory import report_factory
from flask import request
from src.deserializers.json_deserializer import JsonDeserializer
from src.processes.process_factory import process_factory

app = connexion.FlaskApp(__name__)

manager = settings_manager()
manager.open("settings.json")
repository = data_repository()
service = start_service(repository, manager)
service.create()
rep_factory = report_factory(manager)
proc_factory = process_factory()


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
        process_class = proc_factory.get_process('warehouse_turnover_process')

        turnovers = process_class.process(prototype.data)

        report = rep_factory.create_default()
        report.create(turnovers)

        return report.result

    except Exception as ex:
        return Response(f"Ошибка на сервере: {str(ex)}", 500)


@app.route('/settings/block_period', methods=['GET'])
def get_block_period():
    settings = manager.current_settings
    block_period = settings.block_period.strftime("%Y-%m-%d") if settings.block_period else None
    return Response(f"block_period: {block_period}")


@app.route('/settings/new_block_period', methods=['POST'])
def set_block_period():
    try:
        data = request.get_json()
        new_block_period = data.get("block_period")

        if not new_block_period:
            return Response("Дата блокировки не указана!", status=400)

        manager.current_settings.block_period = new_block_period
        manager.save_settings()

        return Response(f"Дата блокировки успешно обновлена. new_block_period: {new_block_period}")

    except Exception as ex:
        return Response(f"Ошибка на сервере: {str(ex)}", status=500)


if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port=8080)
