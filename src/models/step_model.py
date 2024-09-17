class step_model:
    __order: int = 0
    __description: str = ""

    @property
    def order(self):
        return self.__order

    @order.setter
    def order(self, value: int):
        if value <= 0:
            # TODO переделать исключения
            raise ValueError("Порядок шага должен быть положительным числом")
        self.__order = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value: str):
        if len(value) > 1000:
            # TODO переделать исключения
            raise ValueError("Описание шага должно содержать не более 1000 символов")
        self.__description = value
