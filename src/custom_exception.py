class base_exception(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class argument_exception(base_exception):
    def __init__(self, message):
        super().__init__(message)

    @staticmethod
    def raise_type_error(param_name, expected_type):
        raise argument_exception(f"Некорректный тип для параметра '{param_name}'. Ожидается: {expected_type}")

    @staticmethod
    def raise_value_error(param_name, expected_length):
        raise argument_exception(f"Параметр '{param_name}' должен содержать {expected_length} символов")


class operation_exception(base_exception):
    def __init__(self, message):
        super().__init__(message)

    @staticmethod
    def raise_operation_error(operation_name):
        raise operation_exception(f"Ошибка при выполнении операции: {operation_name}")


class error_proxy(base_exception):
    def __init__(self, inner_exception):
        super().__init__(f"Прокси-ошибка: {inner_exception.message}")
        self.inner_exception = inner_exception
