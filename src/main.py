import json
import os

class settings:
    __organization_name = ""
    __inn = ""
    __account_number = ""
    __correspondent_account = ""
    __bik = ""
    __ownership_type = ""

    @property
    def organization_name(self):
        return self.__organization_name

    @organization_name.setter
    def organization_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно передан параметр")
        self.__organization_name = value

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно передан параметр")
        if len(value) != 12:
            raise ValueError("ИНН должен содержать 12 символов")
        self.__inn = value

    @property
    def account_number(self):
        return self.__account_number

    @account_number.setter
    def account_number(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно передан параметр")
        if len(value) != 11:
            raise ValueError("Счет должен содержать 11 символов")
        self.__account_number = value

    @property
    def correspondent_account(self):
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно передан параметр")
        if len(value) != 11:
            raise ValueError("Корреспондентский счет должен содержать 11 символов")
        self.__correspondent_account = value

    @property
    def bik(self):
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        if not isinstance(value, str) or len(value) != 9:
            raise TypeError("Некорректно передан параметр")
        if len(value) != 9:
            raise ValueError("БИК должен содержать 9 символов")
        self.__bik = value

    @property
    def ownership_type(self):
        return self.__ownership_type

    @ownership_type.setter
    def ownership_type(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно передан параметр")
        if len(value) != 5:
            raise ValueError("Вид собственности должен содержать 5 символов")
        self.__ownership_type = value


class settings_manager:
    __file_name = "settings.json"
    __settings: settings = settings()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def open(self, file_path: str = ""):
        if not isinstance(file_path, str):
            raise TypeError("Некорректно передан параметр!")

        if file_path == "":
            file_path = os.path.join(os.curdir, self.__file_name)

        if not os.path.isfile(file_path):
            print(f"Файл '{file_path}' не существует.")
            self.__settings = self.__default_settings()
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as stream:
                data = json.load(stream)
                self.convert(data)
            return True
        except json.JSONDecodeError:
            print("Ошибка разбора JSON.")
        except IOError:
            print("Ошибка открытия файла.")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

        self.__settings = self.__default_settings()
        return False

    def convert(self, data: dict):
        for key, value in data.items():
            if hasattr(self.__settings, key):
                setattr(self.__settings, key, value)

    @property
    def settings(self):
        return self.__settings

    def __default_settings(self):
        data = settings()
        data.inn = "380000000038"
        data.organization_name = "Рога и копыта (default)"
        return data


# Пример использования
manager1 = settings_manager()
manager1.open("settings.json")
print(f"settings1 {manager1.settings.inn}")

manager2 = settings_manager()
# manager2.open("settings1.json")
print(f"settings2 {manager2.settings.inn}")





