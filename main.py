import connexion
from flask import Response
from src.core.format_reporting import format_reporting
from src.data_repository import data_repository
from src.settings_manager import settings_manager
from src.start_service import start_service
from src.reports.report_factory import report_factory

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
    # data = {
    #     'nomenclature': data_repository.nomenclature_key(),
    #     'group_nomenclature': data_repository.group_key(),
    #     'range': data_repository.range_key(),
    #     'recipe': data_repository.recipe_key()
    # }

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


if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port=8080)
