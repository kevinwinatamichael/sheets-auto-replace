import unittest

from client import Client
from creds import Creds


class ClientTestUtils:
    @staticmethod
    def create_spreadsheet():
        service = Creds.get_service()
        spreadsheet = {
            'properties': {
                'title': 'dummy_title'
            }
        }
        return service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()


class ClientTestCases(unittest.TestCase):

    def test_constructor(self):
        sheet_id = 'dummy_id'
        sheet_name = 'dummy_name'
        client = Client(sheet_id=sheet_id, sheet_name=sheet_name)
        expected_service = Creds.get_service()
        self.assertEqual(sheet_id, client._sheet_id)
        self.assertEqual(sheet_name, client._sheet_name)
        self.assertEqual(expected_service.__class__.__name__, client._service.__class__.__name__)

    def test_set_cell(self):
        spreadsheet_id = ClientTestUtils.create_spreadsheet().get('spreadsheetId')
        sheet_name = 'Sheet1'  # default sheet name
        # TODO complete


if __name__ == '__main__':
    unittest.main()
