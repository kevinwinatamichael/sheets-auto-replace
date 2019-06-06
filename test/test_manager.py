import unittest

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
            'keywordRange': Constants.manager_test_keyword_range
        }
        Manager.main(args)


if __name__ == '__main__':
    unittest.main()
