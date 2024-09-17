from DesignPatterns.src.abstract_reference import abstract_reference


class group_nomenclature_model(abstract_reference):
    def __init__(self):
        super().__init__()

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)
