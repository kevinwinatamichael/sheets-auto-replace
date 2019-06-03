import unittest

from cell import Cell
from client import Client
from creds import Creds


class ClientTestUtils:
    def __init__(self, spreadsheet_id):
        self.service = Creds.get_service()
        self.spreadsheet_id = spreadsheet_id

    def clear_spreadsheet(self):
        sheet_id_list = ClientTestUtils.get_sheet_id_list(self.spreadsheet_id)

        self.create_new_sheet()

        request = []
        for sheet_id in sheet_id_list:
            request.append(
                {
                    "deleteSheet": {
                        "sheetId": sheet_id
                    }
                }
            )
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={
                "requests": request
            }
        ).execute()

    def get_sheet_id_list(self):
        response = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        sheets_list = response['sheets']
        sheet_id_list = []
        for sheet in sheets_list:
            sheet_id_list.append(sheet['properties']['sheetId'])
        return sheet_id_list

    def create_new_sheet(self):
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={
                "requests": [
                    {
                        "addSheet": {
                            "properties": {
                                "title": "UNIT TEST",
                                "gridProperties": {
                                    "rowCount": 100,
                                    "columnCount": 20
                                }
                            }
                        }
                    }
                ]
            }
        ).execute()

    def read_cell(self, range_):
        request = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=range_)
        response = request.execute()
        return response['values']


class ClientTestCases(unittest.TestCase):

    def setUp(self) -> None:
        self.spreadsheet_id = '1E5AbARR9-wF23aZbsnbnNaz59pGI7-vjmOiiAf7ck5w'
        self.sheet_name = 'UNIT TEST'
        self.util = ClientTestUtils(self.spreadsheet_id)
        self.util.clear_spreadsheet()

    def test_constructor(self):
        sheet_id = 'dummy_id'
        sheet_name = 'dummy_name'
        client = Client(sheet_id=sheet_id, sheet_name=sheet_name)
        expected_service = Creds.get_service()
        self.assertEqual(sheet_id, client._sheet_id)
        self.assertEqual(sheet_name, client._sheet_name)
        self.assertEqual(expected_service.__class__.__name__, client._service.__class__.__name__)

    def test_set_cell(self):
        client = Client(sheet_id=self.spreadsheet_id, sheet_name=self.sheet_name)
        sheet_range = 'A1:B2'
        exp_values = [[Cell("foo"), Cell("bar")], [Cell("baz")]]

        client.set(sheet_range, exp_values)

        values = self.util.read_cell('A1:B2')

        for row in values:
            self.assertCountEqual(exp_values, values)


if __name__ == '__main__':
    unittest.main()
