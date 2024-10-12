import connexion
from flask import Response
from src.core.format_reporting import format_reporting
from src.data_repository import data_repository
from src.dto.filter_options import filter_option
from src.logics.model_prototype import model_prototype
from src.settings_manager import settings_manager
from src.start_service import start_service
from src.reports.report_factory import report_factory
from src.dto.filter import filter
from flask import request

app = connexion.FlaskApp(__name__)

manager = settings_manager()
manager.open("settings.json")
repository = data_repository()
service = start_service(repository, manager)
service.create()
factory = report_factory(manager)


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
        report = factory.create(report_format)
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
        filter_dto = request.get_json()
        filter_obj = filter()

        filter_obj.name = filter_dto.get('name', "")
        filter_obj.id = filter_dto.get('id', "")

        if filter_dto.get('name_filter_option', "").upper() not in filter_option.__members__:
            return Response("Неправильный тип фильтра для name_filter_option", 400)

        if filter_dto.get('id_filter_option', "").upper() not in filter_option.__members__:
            return Response("Неправильный тип фильтра для id_filter_option", 400)

        # filter_obj.name_filter_option = filter_option[filter_dto.get('name_filter_option', 'EQUAL').upper()]
        name = filter_dto.get('name_filter_option', 'EQUAL').upper()
        filter_obj.name_filter_option = getattr(filter_option, name, filter_option.EQUAL)

        # filter_obj.id_filter_option = filter_option[filter_dto.get('id_filter_option', 'EQUAL').upper()]
        id = filter_dto.get('id_filter_option', 'EQUAL').upper()
        filter_obj.id_filter_option = getattr(filter_option, id, filter_option.EQUAL)

        data = repository.data[category]
        prototype = model_prototype(data)
        result = prototype.create(data, filter_obj)

        # serialized_data = [item.to_dict() for item in result.data]
        #
        # return Response({"result": serialized_data}, 200, mimetype='application/json')

        # #return Response({"result": result.data}, 200)

        report = factory.create_default()
        report.create(prototype.data)

        return report.result


    except Exception as ex:
        return Response(
            f"Ошибка на сервере: {str(ex)}", 500)


if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port=8080)