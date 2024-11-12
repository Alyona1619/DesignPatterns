from src.core.validator import validator
from src.core.filter_options import filter_option


class filter_by_option:

    def __init__(self, option: filter_option):
        validator.validate(option, filter_option)
        self.filtration = getattr(self, option.value.lower())

    @staticmethod
    def equal(first_arg: str, second_arg: str):
        validator.validate(first_arg, str)
        validator.validate(second_arg, str)
        return first_arg == second_arg

    @staticmethod
    def like(part_element: str, element: str):
        validator.validate(part_element, str)
        validator.validate(element, str)
        return part_element in element
