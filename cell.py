class Cell:
    allowed_types = (int, str, float)

    def __init__(self, value):
        if not (isinstance(value, Cell.allowed_types)):
            raise TypeError("Cell value must be in {}".format(Cell.allowed_types))
        self.value = value

    def __repr__(self):
        return "<< Cell: {} [{}] >>".format(self.value, type(self.value))

    def __eq__(self, other):
        return self.value == other.value
