import copy

from cell import Cell


class FormattedCell(Cell):
    def __init__(self, value, bgColor, bold):
        super(FormattedCell, self).__init__(value)

        if not isinstance(bgColor, dict):
            raise TypeError("bgColor must be dictionary")

        if not isinstance(bold, bool):
            raise TypeError("bold must be boolean")

        colors = ["red", "green", "blue"]
        for color in colors:
            if color not in bgColor.keys():
                bgColor[color] = 0

        for v in bgColor.values():
            if not isinstance(v, (int, float)):
                raise TypeError("bgColor value must be int or float")
            if not 0 <= v <= 1:
                raise ValueError("bgColor value must be between 0 and 1")

        self.bgColor = copy.deepcopy(bgColor)
        self.bold = bold

    def __repr__(self):
        return "<< FormattedCell: {} [{}], {}, bold: {} >>".format(self.value, type(self.value), self.bgColor, self.bold)