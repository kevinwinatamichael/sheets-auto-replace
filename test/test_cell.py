import unittest

from cell import Cell
from formatted_cell import FormattedCell


class CellTestCase(unittest.TestCase):
    def test_good_init(self):
        values = [1, "foo", -0.1234]
        for v in values:
            c = Cell(v)
            self.assertEqual(v, c.value)

    def test_bad_init(self):
        values = [int, Cell, {}, [], None]
        for v in values:
            try:
                c = Cell(v)
            except TypeError:
                pass
            else:
                self.fail("Expected error")


class FormattedCellTestCase(unittest.TestCase):
    def test_good_init(self):
        value = "foo"
        bgColors = [
            {"red": 1, "blue": 1, "green": 1},
            {"red": 0.134, "blue": 0.999, "green": 0}
        ]
        bolds = [True, False]
        for bgColor in bgColors:
            for bold in bolds:
                c = FormattedCell(value, bgColor, bold)
                for color in bgColor:
                    self.assertEqual(bgColor[color], c.bgColor[color])
                self.assertEqual(bold, c.bold)

    def test_bad_init(self):
        value = "foo"
        bgColors = [
            {"red": 1, "blue": 1, "green": 1},
            {"red": -0.134, "blue": 0.999, "green": 0},
            {"red": "foo", "blue": 1, "green": 1},
            {"red": 1, "blue": {}, "green": 1},
            {"red": 1, "blue": {}},
        ]
        bolds = [
            True, [], {}, 0, FormattedCell
        ]
        for i, bgColor in enumerate(bgColors):
            for j, bold in enumerate(bolds):
                if i == 0 and j == 0:
                    continue
                try:
                    c = FormattedCell(value, bgColor, bold)
                except TypeError:
                    pass
                except ValueError:
                    pass
                except KeyError:
                    pass
                else:
                    self.fail("Expected error")


if __name__ == '__main__':
    unittest.main()
