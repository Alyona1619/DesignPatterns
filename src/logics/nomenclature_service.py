from src.deserializers.json_deserializer import JsonDeserializer
from src.logics.model_prototype import model_prototype
from src.models.nomenclature_model import nomenclature_model
from src.models.group_nomenclature_model import group_nomenclature_model
from src.models.range_model import range_model
from src.dto.filter import filter
from src.data_repository import data_repository
from src.core.validator import validator, argument_exception, operation_exception


class nomenclature_service:

    def __init__(self, repository: data_repository):
        self.repository = repository

    def add_nomenclature(self, des_nomenclature: nomenclature_model):
        """Метод для добавления новой номенклатуры"""
        try:
            validator.validate(des_nomenclature.full_name, str, 255)
            validator.validate(des_nomenclature.group, group_nomenclature_model)
            validator.validate(des_nomenclature.unit, range_model)

            new_nomenclature = nomenclature_model.default_nomenclature(
                des_nomenclature.full_name, des_nomenclature.group, des_nomenclature.unit
            )

            self.repository.data[data_repository.nomenclature_key()].append(new_nomenclature)
            return new_nomenclature

        except argument_exception as e:
            raise argument_exception(f"Ошибка добавления номенклатуры: {str(e)}")
        except Exception as e:
            raise operation_exception(f"Ошибка выполнения операции добавления номенклатуры: {str(e)}")

    def update_nomenclature(self, filter_obj: filter, des_updated_data: nomenclature_model):
        """Метод для изменения данных существующей номенклатуры"""
        try:
            validator.validate(des_updated_data, nomenclature_model)
            validator.validate(filter_obj, filter)

            prototype = model_prototype(self.repository.data[data_repository.nomenclature_key()])
            filtered_data = prototype.create(self.repository.data[data_repository.nomenclature_key()], filter_obj).data

            if not filtered_data:
                raise operation_exception("Номенклатура не найдена для изменения")

            nomenclature_to_update = filtered_data[0]

            if des_updated_data.full_name:
                validator.validate(des_updated_data.full_name, str, 255)
                nomenclature_to_update.full_name = des_updated_data.full_name
            if des_updated_data.group:
                validator.validate(des_updated_data.group, group_nomenclature_model)
                nomenclature_to_update.group = des_updated_data.group
            if des_updated_data.unit:
                validator.validate(des_updated_data.unit, range_model)
                nomenclature_to_update.unit = des_updated_data.unit

            return nomenclature_to_update

        except argument_exception as e:
            raise argument_exception(f"Ошибка обновления номенклатуры: {str(e)}")
        except operation_exception as e:
            raise operation_exception(f"Ошибка операции обновления: {str(e)}")
        except Exception as e:
            raise operation_exception(f"Ошибка выполнения операции обновления номенклатуры: {str(e)}")

    def get_nomenclature(self, id):
        """Метод для получения номенклатуры"""
        try:
            filter_data = {
                "name": "",
                "id": id,
                "filter_option": "equal"
            }
            filter_obj = JsonDeserializer.deserialize(filter_data, 'filter')
            validator.validate(filter_obj, filter)

            prototype = model_prototype(self.repository.data[data_repository.nomenclature_key()])
            filtered_data = prototype.create(self.repository.data[data_repository.nomenclature_key()], filter_obj)

            if not filtered_data:
                raise operation_exception("Номенклатура не найдена")

            return filtered_data

        except argument_exception as e:
            raise argument_exception(f"Ошибка получения номенклатуры: {str(e)}")
        except operation_exception as e:
            raise operation_exception(f"Ошибка операции получения номенклатуры: {str(e)}")
        except Exception as e:
            raise operation_exception(f"Ошибка выполнения операции получения номенклатуры: {str(e)}")

    def delete_nomenclature(self, filter_obj: filter):
        """Метод для удаления номенклатуры"""
        try:
            validator.validate(filter_obj, filter)

            prototype = model_prototype(self.repository.data[data_repository.nomenclature_key()])
            filtered_data = prototype.create(self.repository.data[data_repository.nomenclature_key()], filter_obj).data

            if not filtered_data:
                raise operation_exception("Номенклатура не найдена для удаления")

            nomenclature_to_delete = filtered_data[0]
            self.repository.data[data_repository.nomenclature_key()].remove(nomenclature_to_delete)
            return nomenclature_to_delete

        except argument_exception as e:
            raise argument_exception(f"Ошибка удаления номенклатуры: {str(e)}")
        except operation_exception as e:
            raise operation_exception(f"Ошибка операции удаления номенклатуры: {str(e)}")
        except Exception as e:
            raise operation_exception(f"Ошибка выполнения операции удаления номенклатуры: {str(e)}")
