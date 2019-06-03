from cell import Cell


class FormattedCell(Cell):
    def __init__(self, value, bgColor, bold):
        super(FormattedCell, self).__init__(value)

        if not isinstance(bgColor, dict):
            raise TypeError("bgColor must be dictionary")

        if not isinstance(bold, bool):
            raise TypeError("bold must be boolean")

        if {"red", "green", "blue"}.issubset(set(bgColor.keys())):
            raise KeyError("bgColor must contain red, green, and blue keys")

        for v in bgColor.values():
            if not isinstance(v, (int, float)):
                raise TypeError("bgColor value must be int or float")
            if not 0 <= v <= 1:
                raise ValueError("bgColor value must be between 0 and 1")

        self.bgColor = bgColor
        self.bold = bold
