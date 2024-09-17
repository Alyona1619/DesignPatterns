class ingredient_model:
    __name: str = ""
    __amount: str = ""

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        if len(value) > 255:
            # TODO переделать исключения
            raise ValueError("Название ингредиента должно содержать не более 255 символов")
        self.__name = value

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value: str):
        self.__amount = value
