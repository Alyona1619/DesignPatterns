import xml.etree.ElementTree as ET
from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.core.validator import validator, operation_exception


class xml_report(abstract_report):
    """Ответ формирует набор данных в формате XML"""

    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.XML

    def create(self, data: list):
        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Набор данных пуст!")

        # Создаем корневой элемент
        root = ET.Element("Reports")

        for row in data:
            row_element = ET.SubElement(root, "Report")
            fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(row.__class__, x)),
                                 dir(row)))
            for field in fields:
                field_value = getattr(row, field)
                field_element = ET.SubElement(row_element, field)
                field_element.text = str(field_value)

        # Преобразуем дерево XML в строку
        self.result = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')

