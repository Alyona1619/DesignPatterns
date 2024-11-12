class argument_exception(Exception):
    """Исключение при проверки аргумента"""
    pass


class operation_exception(Exception):
    """Исключение при выполнении бизнес операции"""
    pass


class validator:
    """Набор проверок данных"""

    @staticmethod
    def validate(value, type_, len_=None):
        """
            Валидация аргумента по типу и длине
        Args:
            value (any): Аргумент
            type_ (object): Ожидаемый тип
            len_ (int): Максимальная длина
        Raises:
            arguent_exception: Некорректный тип
            arguent_exception: Неулевая длина
            arguent_exception: Некорректная длина аргумента
        Returns:
            True или Exception
        """

        if value is None:
            raise argument_exception(f"Пустой аргумент {type(value)}")

        # Проверка типа
        # if not isinstance(value, type_):
        #     raise argument_exception("Некорректный тип")
        if isinstance(type_, type):
            if not isinstance(value, type_):
                raise argument_exception(f"Некорректный тип. Ожидался {type_}, получен {type(value)}.")
        else:
            raise argument_exception("Передан некорректный тип для проверки.")

        # Проверка аргумента
        if len(str(value).strip()) == 0:
            raise argument_exception(f"Пустой аргумент {type(value)}")

        if len_ is not None and len(str(value).strip()) >= len_:
            raise argument_exception("Некорректная длина аргумента")

        return True
