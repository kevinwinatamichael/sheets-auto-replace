import unittest

from cell import Cell
from formatted_cell import FormattedCell
from manager import Manager
from test.constants import Constants


class ManagerTestCases(unittest.TestCase):

    def test_sanity(self):
        args = {
            'reviewSheetId': Constants.manager_test_review_spreadsheet_id,
            'reviewSheetName': Constants.manager_test_review_sheet_name,
            'keywordSheetId': Constants.manager_test_keyword_spreadsheet_id,
            'keywordSheetName': Constants.manager_test_keyword_sheet_name,
            'reviewRange': Constants.manager_test_review_range,
            'keywordRange': Constants.manager_test_keyword_range,
            'interval': 2,
        }
        Manager.main(args)


class Test_get_indices_to_replace(unittest.TestCase):
    """
        Flowchart:
        for: (1)
            if: (2)
                code (3)
        return

        Basis paths:
        1. 1,2,3
        2. 1,2
        3. 1
    """
    PLAIN_CELL = FormattedCell("val", {'red':1, 'blue':1, 'green':1}, False)
    COLOR_CELL = FormattedCell("val", {'red':0.5, 'blue':1, 'green':1}, False)

    def test_basis_1(self):
        data = [
            [self.COLOR_CELL]
        ]
        self.assertCountEqual([0], Manager.get_indices_to_replace(data))

    def test_basis_2(self):
        data = [
            [self.PLAIN_CELL]
        ]
        self.assertCountEqual([], Manager.get_indices_to_replace(data))

    def test_basis_3(self):
        data = []
        self.assertCountEqual([], Manager.get_indices_to_replace(data))

class Test_get_keyword_replacement(unittest.TestCase):
    """
        Flowchart:
        for: (1)
            if: continue (2)
            if: commands (3)
        if: raise (4)
        return
        Y annotate enter, N annotate not enter
        Basis paths:
        1. 1,2,1,3
        2. 1,2,1,3,4
        3. 1,2,1
        4. 1,3,1
        5. 1
    """
    def test_sanity(self):
        number_of_replacement = 2
        data = [
            [Cell("keyword1"), Cell(1)],
            [Cell("keyword2"), Cell(1)],
            [Cell("keyword3")],
            [Cell("keyword4")],
            [Cell("keyword5")]
        ]
        keyword_terms, keyword_indices = Manager.get_keyword_replacement(number_of_replacement, data)
        self.assertCountEqual(["keyword3", "keyword4"], keyword_terms)
        self.assertCountEqual([2, 3], keyword_indices)

    def test_basis_1(self):
        number_of_replacement = 1
        data = [
            [Cell("keyword1"), Cell(1)],
            [Cell("keyword2")],
        ]
        keyword_terms, keyword_indices = Manager.get_keyword_replacement(number_of_replacement, data)
        self.assertCountEqual(["keyword2"], keyword_terms)
        self.assertCountEqual([1], keyword_indices)

    def test_basis_2(self):
        number_of_replacement = 2
        data = [
            [Cell("keyword1"), Cell(1)],
            [Cell("keyword2")],
        ]
        try:
            keyword_terms, keyword_indices = Manager.get_keyword_replacement(number_of_replacement, data)
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError")

    def test_basis_3(self):
        number_of_replacement = 0
        data = [
            [Cell("keyword1"), Cell(1)],
        ]
        keyword_terms, keyword_indices = Manager.get_keyword_replacement(number_of_replacement, data)
        self.assertCountEqual([], keyword_terms)
        self.assertCountEqual([], keyword_indices)

    def test_basis_4(self):
        number_of_replacement = 1
        data = [
            [Cell("keyword1")],
        ]
        keyword_terms, keyword_indices = Manager.get_keyword_replacement(number_of_replacement, data)
        self.assertCountEqual(["keyword1"], keyword_terms)
        self.assertCountEqual([0], keyword_indices)

    def test_basis_5(self):
        number_of_replacement = 0
        data = []
        keyword_terms, keyword_indices = Manager.get_keyword_replacement(number_of_replacement, data)
        self.assertCountEqual([], keyword_terms)
        self.assertCountEqual([], keyword_indices)

if __name__ == '__main__':
    unittest.main()
