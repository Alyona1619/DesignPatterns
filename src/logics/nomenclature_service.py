from src.core.abstract_logic import abstract_logic
from src.core.event_type import event_type
from src.core.validator import validator, argument_exception, operation_exception
from src.data_repository import data_repository
from src.deserializers.json_deserializer import JsonDeserializer
from src.dto.filter import filter
from src.logics.model_prototype import model_prototype
from src.logics.observe_service import observe_service
from src.models.nomenclature_model import nomenclature_model


class nomenclature_service(abstract_logic):

    def __init__(self, repository: data_repository):
        self.repository = repository
        observe_service.append(self)

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

            filtered_data = model_prototype(self.repository.data[data_repository.nomenclature_key()]).create(
                self.repository.data[data_repository.nomenclature_key()], filter_obj)
            print(filtered_data.data)
            if len(filtered_data.data) == 0:
                raise operation_exception("Номенклатура не найдена")

            return filtered_data

        except argument_exception as e:
            raise argument_exception(f"Ошибка получения номенклатуры: {str(e)}")
        except operation_exception as e:
            raise operation_exception(f"Ошибка операции получения номенклатуры: {str(e)}")
        except Exception as e:
            raise operation_exception(f"Ошибка выполнения операции получения номенклатуры: {str(e)}")

    def add_nomenclature(self, data):
        """Метод для добавления новой номенклатуры"""
        try:
            des_nomenclature = JsonDeserializer.deserialize(data, 'nomenclature_model')

            filter_data = {
                "name": des_nomenclature.full_name,
                "filter_option": "equal"
            }
            filter_obj = JsonDeserializer.deserialize(filter_data, 'filter')

            existing_nomenclature = model_prototype(self.repository.data[data_repository.nomenclature_key()]).create(
                self.repository.data[data_repository.nomenclature_key()], filter_obj)

            if existing_nomenclature.data:
                raise operation_exception("Номенклатура уже существует и не может быть добавлена повторно")

            new_nomenclature = nomenclature_model.default_nomenclature(
                des_nomenclature.full_name, des_nomenclature.group, des_nomenclature.unit
            )

            self.repository.data[data_repository.nomenclature_key()].append(new_nomenclature)
            return new_nomenclature

        except argument_exception as e:
            raise argument_exception(f"Ошибка добавления номенклатуры: {str(e)}")
        except Exception as e:
            raise operation_exception(f"Ошибка выполнения операции добавления номенклатуры: {str(e)}")

    def update_nomenclature(self, data):
        """Метод для изменения данных существующей номенклатуры"""
        try:
            unique_code = data.get('unique_code')
            if not unique_code:
                raise operation_exception("Не указан уникальный код номенклатуры.")

            filter_data = {
                "name": "",
                "id": unique_code,
                "filter_option": "equal"
            }
            filter_obj = JsonDeserializer.deserialize(filter_data, 'filter')
            validator.validate(filter_obj, filter)

            nomenclature_data = model_prototype(self.repository.data[data_repository.nomenclature_key()]).create(
                self.repository.data[data_repository.nomenclature_key()], filter_obj)

            if not nomenclature_data:
                raise operation_exception(f"Номенклатура с уникальным кодом {unique_code} не найдена.")

            nomenclature = nomenclature_data.data[0]

            if 'full_name' in data:
                nomenclature.full_name = data['full_name']

            if 'group_id' in data:
                group_id = data['group_id']
                group_filter = {
                    "id": group_id,
                    "filter_option": "equal"
                }
                group_filter_obj = JsonDeserializer.deserialize(group_filter, 'filter')
                validator.validate(group_filter_obj, filter)

                group_data = model_prototype(self.repository.data[data_repository.group_key()]).create(
                    self.repository.data[data_repository.group_key()], group_filter_obj)

                if group_data:
                    nomenclature.group = group_data[0]

            if 'unit_id' in data:
                unit_id = data['unit_id']
                unit_filter = {
                    "id": unit_id,
                    "filter_option": "equal"
                }
                unit_filter_obj = JsonDeserializer.deserialize(unit_filter, 'filter')
                validator.validate(unit_filter_obj, filter)

                unit_data = model_prototype(self.repository.data[data_repository.range_key()]).create(
                    self.repository.data[data_repository.range_key()], unit_filter_obj)

                if unit_data:
                    nomenclature.unit = unit_data[0]

            observe_service.raise_event(event_type.CHANGE_NOMENCLATURE_IN_RECIPE, data)
            observe_service.raise_event(event_type.CHANGE_NOMENCLATURE_IN_TURNOVER, data)

            return nomenclature

        except operation_exception as e:
            raise operation_exception(f"Ошибка обновления номенклатуры: {str(e)}")
        except Exception as e:
            raise operation_exception(f"Ошибка выполнения операции обновления номенклатуры: {str(e)}")

    def update_applied_nomenclature(self, obj, data):
        unique_code = data.get('unique_code')
        if hasattr(obj, 'unique_code') and obj.unique_code == unique_code:
            if 'name' in data:
                obj.name = data['name']
            if 'full_name' in data:
                obj.full_name = data['full_name']

            if 'group_id' in data:
                group_id = data['group_id']
                group_filter = {
                    "id": group_id,
                    "filter_option": "equal"
                }
                group_filter_obj = JsonDeserializer.deserialize(group_filter, 'filter')
                validator.validate(group_filter_obj, filter)

                group_data = model_prototype(self.repository.data[data_repository.group_key()]).create(
                    self.repository.data[data_repository.group_key()], group_filter_obj)

                if group_data:
                    obj.group = group_data[0]

            if 'range_id' in data:
                unit_id = data['unit_id']
                unit_filter = {
                    "id": unit_id,
                    "filter_option": "equal"
                }
                unit_filter_obj = JsonDeserializer.deserialize(unit_filter, 'filter')
                validator.validate(unit_filter_obj, filter)

                unit_data = model_prototype(self.repository.data[data_repository.range_key()]).create(
                    self.repository.data[data_repository.range_key()], unit_filter_obj)

                if unit_data:
                    obj.unit = unit_data[0]

            return True

        if isinstance(obj, dict):
            for key, value in obj.items():
                if self.update_applied_nomenclature(value, data):
                    return True
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                if self.update_applied_nomenclature(item, data):
                    return True
        elif hasattr(obj, '__dict__'):
            for attr_name in vars(obj):
                attr_value = getattr(obj, attr_name)
                if self.update_applied_nomenclature(attr_value, data):
                    return True

        return False

    def delete_nomenclature(self, data):
        """Метод для удаления номенклатуры"""
        try:
            id = data.get("unique_code")
            if not id:
                raise operation_exception("Не указан уникальный код  для удаления")
            filter_data = {
                "id": id,
                "filter_option": "equal"
            }
            filter_obj = JsonDeserializer.deserialize(filter_data, 'filter')
            validator.validate(filter_obj, filter)

            prototype = model_prototype(self.repository.data[data_repository.nomenclature_key()])
            filtered_data = prototype.create(self.repository.data[data_repository.nomenclature_key()], filter_obj)

            if not filtered_data:
                raise operation_exception("Номенклатура не найдена для удаления")

            nomenclature_to_delete = filtered_data.data[0]

            if self.is_nomenclature_in_recipes(nomenclature_to_delete):
                raise operation_exception(
                    f"Номенклатура '{id}' не может быть удалена. Она используется в рецептах")

            if self.is_nomenclature_in_turnovers(nomenclature_to_delete):
                raise operation_exception(
                    f"Номенклатура '{id}' не может быть удалена. Она используется в сохраненных оборотах")

            self.repository.data[data_repository.nomenclature_key()].remove(nomenclature_to_delete)

        except argument_exception as e:
            raise argument_exception(f"Ошибка удаления номенклатуры: {str(e)}")
        except operation_exception as e:
            raise operation_exception(f"Ошибка операции удаления номенклатуры: {str(e)}")
        except Exception as e:
            raise operation_exception(f"Ошибка выполнения операции удаления номенклатуры: {str(e)}")

    def is_nomenclature_in_recipes(self, nomenclature: nomenclature_model) -> bool:
        print(type(nomenclature.unique_code))
        filter_data = {
            "id": nomenclature.unique_code,
            "filter_option": "equal"
        }
        filter_obj = JsonDeserializer.deserialize(filter_data, 'filter')

        filtered_recipes = model_prototype(self.repository.data[data_repository.recipe_key()]).create(
            self.repository.data[data_repository.recipe_key()], filter_obj)

        return len(filtered_recipes.data) != 0

    def is_nomenclature_in_turnovers(self, nomenclature: nomenclature_model) -> bool:
        filter_data = {
            "id": nomenclature.unique_code,
            "filter_option": "equal"
        }
        filter_obj = JsonDeserializer.deserialize(filter_data, 'filter')

        filtered_recipes = model_prototype(self.repository.data[data_repository.blocked_turnover_key()]).create(
            self.repository.data[data_repository.blocked_turnover_key()], filter_obj)

        return len(filtered_recipes.data) != 0

    def set_exception(self, ex: Exception):
        super().set_exception(ex)

    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)

        if type == event_type.CHANGE_NOMENCLATURE:
            self.update_nomenclature(params)
        elif type == event_type.DELETE_NOMENCLATURE:
            self.delete_nomenclature(params)
