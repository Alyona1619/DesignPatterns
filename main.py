import connexion
from flask import Response
from flask import request

from src.core.event_type import event_type
from src.core.format_reporting import format_reporting
from src.data_repository import data_repository
from src.deserializers.json_deserializer import JsonDeserializer
from src.logics.logging import logging
from src.logics.model_prototype import model_prototype
from src.logics.nomenclature_service import nomenclature_service
from src.logics.observe_service import observe_service
from src.logics.transaction_prototype import transaction_prototype
from src.processes.process_factory import process_factory
from src.processes.wh_blocked_turnover_process import warehouse_blocked_turnover_process
from src.processes.wh_turnover_process import warehouse_turnover_process
from src.reports.report_factory import report_factory
from src.repository_manager import repository_manager
from src.settings_manager import settings_manager
from src.start_service import start_service

app = connexion.FlaskApp(__name__)

manager = settings_manager()
manager.open("settings.json")
repository = data_repository()
repository.data[data_repository.blocked_turnover_key()] = {}
rep_manager = repository_manager(repository, manager)
service = start_service(repository, manager, rep_manager)
service.create()
rep_factory = report_factory(manager)
proc_factory = process_factory()
nomenclature_serv = nomenclature_service(repository)

logging = logging(manager)


@app.route("/api/reports/formats", methods=["GET"])
def formats():
    observe_service.raise_event(event_type.LOG_DEBUG, params="Запрос: /api/reports/formats [GET]")
    result = []
    for report in format_reporting:
        result.append({"name": report.name, "value": report.value})
    observe_service.raise_event(event_type.LOG_INFO, params="Список форматов успешно возвращен")

    return result


@app.route("/api/reports/<category>/<format>", methods=["GET"])
def get_report(category, format):
    observe_service.raise_event(event_type.LOG_DEBUG, params=f"Запрос: /api/reports/{category}/{format} [GET]")

    data_methods = [method for method in dir(data_repository) if
                    callable(getattr(data_repository, method)) and method.endswith('_key')]
    data = {method.replace('_key', ''): getattr(data_repository, method)() for method in data_methods}

    if category not in data:
        observe_service.raise_event(event_type.LOG_ERROR, params=f"Неверная категория: {category}")

        return Response(f"Указанная категория '{category}' отсутствует!", 400)

    try:
        report_format = format_reporting[format.upper()]
    except:
        observe_service.raise_event(event_type.LOG_ERROR, params=f"Неверные формат: {format}")
        return Response("Указанный формат отчёта отсутствует!", 400)

    try:
        report = rep_factory.create(report_format)
        report.create(repository.data[data[category]])

        observe_service.raise_event(event_type.LOG_INFO, params=f"Отчет для {category} успешно создан")

    except Exception as ex:
        observe_service.raise_event(event_type.LOG_ERROR, params=f"Ошибка во время создания отчета: {str(ex)}")
        return Response(f"Ошибка на сервере! {str(ex)}", 500)

    return Response(report.result, 200)


@app.route("/api/filter/<category>", methods=["POST"])
def filter_data(category):
    observe_service.raise_event(event_type.LOG_DEBUG, params=f"Запрос: /api/filter/{category} [POST]")

    data_methods = [method for method in dir(data_repository) if
                    callable(getattr(data_repository, method)) and method.endswith('_key')]
    categories = {method.replace('_key', ''): getattr(data_repository, method)() for method in data_methods}

    if category not in categories:
        observe_service.raise_event(event_type.LOG_ERROR, params=f"Неверная категория: {category}")

        return Response(f"Указанная категория '{category}' отсутствует!", 400)

    try:
        filter_data = request.get_json()
        observe_service.raise_event(event_type.LOG_DEBUG, params="Десериализация фильтра началась")

        filter_obj = JsonDeserializer.deserialize(filter_data, 'filter')

        prototype = model_prototype(repository.data[category]).create(repository.data[category], filter_obj)
        report = rep_factory.create_default()
        report.create(prototype.data)
        observe_service.raise_event(event_type.LOG_INFO, params=f"Фильтр успешно применен к категории {category}")

        return report.result

    except Exception as ex:
        observe_service.raise_event(event_type.LOG_ERROR, params=f"Ошибка во время фильтрации данных: {str(ex)}")
        return Response(f"Ошибка на сервере: {str(ex)}", 500)


@app.route("/api/warehouse/transactions", methods=["POST"])
def get_warehouse_transactions():
    try:
        observe_service.raise_event(event_type.LOG_INFO, params="Начало обработки запроса /api/warehouse/transactions")

        filter_data = request.get_json()
        observe_service.raise_event(event_type.LOG_DEBUG, params=f"Полученные данные: {filter_data}")

        filter_obj = JsonDeserializer.deserialize(filter_data, 'filter_transaction')
        observe_service.raise_event(event_type.LOG_DEBUG, params=f"Десериализация завершена: {filter_obj}")

        t_data = repository.data[[data_repository.transaction_key()]]
        if not t_data:
            observe_service.raise_event(event_type.LOG_ERROR, params="Данные отсутствуют в репозитории")

            return Response("Нет данных", 400)

        observe_service.raise_event(event_type.LOG_INFO, params=f"Данные из репозитория успешно получены: {t_data}")

        prototype = transaction_prototype(t_data).create(t_data, filter_obj)
        observe_service.raise_event(event_type.LOG_DEBUG, params=f"Прототип создан: {prototype}")

        report = rep_factory.create_default()
        report.create(prototype.data)
        observe_service.raise_event(event_type.LOG_INFO, params="Отчет успешно создан")

        return report.result

    except Exception as ex:
        return Response(f"Ошибка на сервере: {str(ex)}", 500)


@app.route("/api/warehouse/turnover", methods=["POST"])
def get_warehouse_turnover():
    try:
        observe_service.raise_event(event_type.LOG_INFO, params="Начало обработки запроса /api/warehouse/turnover")

        filter_data = request.get_json()
        observe_service.raise_event(event_type.LOG_DEBUG, params=f"Получены данные фильтрации: {filter_data}")

        filter_obj = JsonDeserializer.deserialize(filter_data, 'filter_transaction')
        observe_service.raise_event(event_type.LOG_DEBUG, params=f"Фильтр десериализован: {filter_obj}")

        t_data = repository.data[[data_repository.transaction_key()]]
        if not t_data:
            observe_service.raise_event(event_type.LOG_ERROR,
                                        params="В репозитории отсутствуют данные по ключу транзакции")

            return Response("Нет данных", 400)
        observe_service.raise_event(event_type.LOG_INFO, params="Данные успешно взяты из репозитория")

        prototype = transaction_prototype(t_data).create(t_data, filter_obj)
        observe_service.raise_event(event_type.LOG_DEBUG, params=f"Создан прототип транзакции: {prototype}")

        proc_factory.register_process(warehouse_turnover_process)
        observe_service.raise_event(event_type.LOG_INFO, params="Процесс warehouse_turnover_process зарегистрирован")

        process_class = proc_factory.get_process('warehouse_turnover_process', manager)
        observe_service.raise_event(event_type.LOG_INFO,
                                    params="Процесс warehouse_turnover_process успешно получен из фабрики процессов")

        turnovers = process_class.process(prototype.data)
        observe_service.raise_event(event_type.LOG_DEBUG, params=f"Результат обработки процесса: {turnovers}")

        report = rep_factory.create_default()
        report.create(turnovers)
        observe_service.raise_event(event_type.LOG_INFO, params="Отчет успешно создан")

        return report.result

    except Exception as ex:
        observe_service.raise_event(event_type.LOG_ERROR, params=f"Ошибка на сервере: {str(ex)}")

        return Response(f"Ошибка на сервере: {str(ex)}", 500)


@app.route('/api/settings/block_period', methods=['GET'])
def get_block_period():
    try:
        observe_service.raise_event(event_type.LOG_INFO, params="Начало работы запроса /api/settings/block_period")

        block_period = manager.get_block_period_str()
        observe_service.raise_event(event_type.LOG_DEBUG, params=f"Получен период блокировки: {block_period}")
        observe_service.raise_event(event_type.LOG_INFO, params="Запрос обработан успешно")

        return Response(f"block_period: {block_period}")
    except Exception as ex:
        observe_service.raise_event(event_type.LOG_ERROR, params=f"Ошибка на сервере: {str(ex)}")
        return Response(f"Ошибка на сервере: {str(ex)}", 500)


@app.route('/api/settings/new_block_period', methods=['POST'])
def set_block_period():
    try:
        observe_service.raise_event(event_type.LOG_INFO,
                                    params="Начало обработки запроса /api/settings/new_block_period")

        data = request.get_json()
        new_block_period = data.get("block_period")
        observe_service.raise_event(event_type.LOG_DEBUG, params=f"Получены данные из запроса: {data}")

        if not new_block_period:
            observe_service.raise_event(event_type.LOG_ERROR, params="Дата блокировки не указана!")

            return Response("Дата блокировки не указана!", status=400)

        manager.current_settings.block_period = new_block_period
        observe_service.raise_event(event_type.LOG_INFO, params=f"Дата блокировки обновлена на {new_block_period}")

        observe_service.raise_event(event_type.CHANGE_BLOCK_PERIOD, None)

        transactions = repository.data[data_repository.transaction_key()]
        if not transactions:
            observe_service.raise_event(event_type.LOG_ERROR, params="Нет транзакций для пересчета.")

            return Response("Нет транзакций для пересчета.", status=400)

        observe_service.raise_event(event_type.LOG_DEBUG,
                                    params=f"Найдено {len(transactions)} транзакций для пересчета.")

        proc_factory.register_process(warehouse_blocked_turnover_process)
        process_class = proc_factory.get_process('warehouse_blocked_turnover_process', manager)

        blocked_turnovers = process_class.process(transactions)
        repository.data[data_repository.blocked_turnover_key()] = blocked_turnovers
        observe_service.raise_event(event_type.LOG_INFO,
                                    params=f"Перерасчет завершен. Заблокированных оборотов: {len(blocked_turnovers)}")

        return Response(f"Дата блокировки успешно обновлена. new_block_period: {new_block_period}."
                        f"Заблокированные обороты пересчитаны помещены в репозиторий данных: {len(blocked_turnovers)}",
                        status=200)

    except Exception as ex:
        observe_service.raise_event(event_type.LOG_ERROR, params=f"Ошибка на сервере: {str(ex)}")

        return Response(f"Ошибка на сервере: {str(ex)}", status=500)


@app.route("/api/nomenclature/<id>", methods=["GET"])
def get_nomenclature(id):
    try:
        observe_service.raise_event(event_type.LOG_INFO,
                                    params=f"Запрос получения номенклатуры /api/nomenclature/<id> с ID: {id}")

        nomen = nomenclature_serv.get_nomenclature(id)
        observe_service.raise_event(event_type.LOG_DEBUG,
                                    params=f"Номенклатура с ID {id} успешно получена: {nomen.data}")

        report = rep_factory.create_default()
        report.create(nomen.data)
        observe_service.raise_event(event_type.LOG_INFO, params=f"Отчет для номенклатуры с ID {id} успешно создан")

        return report.result

    except Exception as ex:
        observe_service.raise_event(event_type.LOG_ERROR,
                                    params=f"Ошибка при получении номенклатуры с ID {id}: {str(ex)}")

        return Response(f"Ошибка на сервере: {str(ex)}", status=500)


@app.route("/api/nomenclature", methods=["PUT"])
def add_nomenclature():
    try:
        observe_service.raise_event(event_type.LOG_INFO,
                                    params="Запрос на добавление новой номенклатуры /api/nomenclature")

        data = request.get_json()
        observe_service.raise_event(event_type.LOG_DEBUG, params=f"Данные для добавления номенклатуры: {data}")

        new_nomenclature = nomenclature_serv.add_nomenclature(data)
        observe_service.raise_event(event_type.LOG_INFO,
                                    params=f"Новая номенклатура успешно добавлена: {new_nomenclature}")

        return Response(f"Номенклатура успешно добавлена: {new_nomenclature}", status=200)

    except Exception as ex:
        observe_service.raise_event(event_type.LOG_ERROR, params=f"Ошибка при добавлении номенклатуры: {str(ex)}")

        return Response(f"Ошибка на сервере: {str(ex)}", status=500)


@app.route("/api/nomenclature", methods=["PATCH"])
def update_nomenclature():
    try:
        observe_service.raise_event(event_type.LOG_INFO, params="Запрос на обновление номенклатуры /api/nomenclature")

        data = request.get_json()
        observe_service.raise_event(event_type.LOG_DEBUG, params=f"Данные для обновления номенклатуры: {data}")

        observe_service.raise_event(event_type.CHANGE_NOMENCLATURE, data)

        observe_service.raise_event(event_type.LOG_INFO, params="Номенклатура успешно обновлена")

        return Response(f"Номенклатура успешно обновлена", status=200)

    except Exception as ex:
        observe_service.raise_event(event_type.LOG_ERROR, params=f"Ошибка при обновлении номенклатуры: {str(ex)}")

        return Response(f"Ошибка на сервере: {str(ex)}", status=500)


@app.route("/api/nomenclature", methods=["DELETE"])
def delete_nomenclature():
    try:
        observe_service.raise_event(event_type.LOG_INFO, params="Запрос на удаление номенклатуры /api/nomenclature")

        data = request.get_json()
        observe_service.raise_event(event_type.LOG_DEBUG, params=f"Данные для удаления номенклатуры: {data}")

        observe_service.raise_event(event_type.DELETE_NOMENCLATURE, data)

        observe_service.raise_event(event_type.LOG_INFO, params="Номенклатура успешно удалена")

        return Response(f"Номенклатура успешно удалена", status=200)

    except Exception as ex:
        observe_service.raise_event(event_type.LOG_ERROR, params=f"Ошибка при удалении номенклатуры: {str(ex)}")

        return Response(f"Ошибка на сервере: {str(ex)}", status=500)


@app.route("/api/tbs/<start_date>/<end_date>/<warehouse>", methods=["GET"])
def get_tbs_report(start_date, end_date, warehouse):
    try:
        observe_service.raise_event(event_type.LOG_INFO,
                                    params=f"Запрос на получение Оборотно-сальдовой-ведомости /api/tbs/{start_date}/{end_date}/{warehouse}")

        if not start_date or not end_date or not warehouse:
            observe_service.raise_event(event_type.LOG_ERROR,
                                        params="Отсутствуют необходимые параметры: 'Дата начала', 'Дата окончания', 'Склад'")

            return Response("Необходимо указать 'Дата начала', 'Дата окончания' и 'Склад'.", status=400)

        transactions = repository.data[data_repository.transaction_key()]
        if not transactions:
            observe_service.raise_event(event_type.LOG_ERROR, params="Нет данных транзакций для формирования отчета")

            return Response("Нет данных", 400)

        observe_service.raise_event(event_type.LOG_DEBUG, params=f"Количество транзакций: {len(transactions)}")

        proc_factory.register_process(warehouse_turnover_process)
        # до
        observe_service.raise_event(event_type.LOG_INFO, params=f"Формирование данных оборотов до {start_date}")

        filter_data_before = {
            "warehouse": {
                "name": warehouse,
                "unique_code": "",
                "filter_option": "like"},
            "nomenclature": {
                "name": "",
                "unique_code": "",
                "filter_option": "like"},
            "start_period": "1900-01-01",
            "end_period": start_date
        }
        filter_obj_before = JsonDeserializer.deserialize(filter_data_before, 'filter_transaction')

        transaction_data_before = transaction_prototype(transactions).create(transactions, filter_obj_before)

        turnover_process_class1 = proc_factory.get_process('warehouse_turnover_process', manager)
        turnover_data_before = turnover_process_class1.process(transaction_data_before.data)
        observe_service.raise_event(event_type.LOG_DEBUG,
                                    params=f"Данные оборотов до {start_date} сформированы: {turnover_data_before}")

        # от до
        observe_service.raise_event(event_type.LOG_INFO,
                                    params=f"Формирование данных оборотов с {start_date} до {end_date}")

        filter_data_between = {
            "warehouse": {
                "name": warehouse,
                "unique_code": "",
                "filter_option": "like"},
            "nomenclature": {
                "name": "",
                "unique_code": "",
                "filter_option": "like"},
            "start_period": start_date,
            "end_period": end_date
        }
        filter_obj_between = JsonDeserializer.deserialize(filter_data_between, 'filter_transaction')

        transaction_data_between = transaction_prototype(transactions).create(transactions, filter_obj_between)

        turnover_process_class2 = proc_factory.get_process('warehouse_turnover_process', manager)
        turnover_data_between = turnover_process_class2.process(transaction_data_between.data)
        observe_service.raise_event(event_type.LOG_DEBUG,
                                    params=f"Данные оборотов с {start_date} до {end_date} сформированы: {turnover_data_between}")

        observe_service.raise_event(event_type.LOG_INFO, params="Формирование итогового отчета TBS")

        turnover_data = [turnover_data_before, turnover_data_between]

        report = rep_factory.create(format_reporting.TBS)
        report.create(turnover_data)
        observe_service.raise_event(event_type.LOG_INFO, params="TBS-отчет успешно сформирован")

        return Response(report.result, status=200, mimetype='application/json')

    except Exception as ex:
        observe_service.raise_event(event_type.LOG_ERROR, params=f"Ошибка при формировании TBS-отчета: {str(ex)}")

        return Response(f"Ошибка на сервере: {str(ex)}", status=500)


@app.route("/api/save_data", methods=["POST"])
def save_data():
    try:
        observe_service.raise_event(event_type.LOG_INFO, params="Начало процесса сохранения данных.")

        observe_service.raise_event(event_type.SAVE_DATA, None)

        observe_service.raise_event(event_type.LOG_INFO, params="Данные успешно сохранены в файл.")

        return Response("Данные успешно сохранены в файл.", status=200)

    except Exception as ex:
        observe_service.raise_event(event_type.LOG_ERROR, params=f"Ошибка при сохранении данных: {str(ex)}")

        return Response(f"Ошибка при сохранении данных: {str(ex)}", status=500)


@app.route("/api/load_data", methods=["POST"])
def load_data():
    try:
        observe_service.raise_event(event_type.LOG_INFO, params="Начало процесса загрузки данных.")

        observe_service.raise_event(event_type.LOAD_DATA, None)

        observe_service.raise_event(event_type.LOG_INFO, params="Данные успешно восстановлены из файла.")

        return Response("Данные успешно восстановлены из файла.", status=200)

    except Exception as ex:
        observe_service.raise_event(event_type.LOG_ERROR, params=f"Ошибка при восстановлении данных: {str(ex)}")
        return Response(f"Ошибка при восстановлении данных: {str(ex)}", status=500)


if __name__ == '__main__':
    observe_service.raise_event(event_type.LOG_INFO, params="Запуск FastAPI")
    app.add_api("swagger.yaml")
    app.run(port=8080)
