import time
import unittest

from cell import Cell
from client import Client
from creds import Creds
from formatted_cell import FormattedCell
from test.constants import Constants


class ClientTestUtils:
    def __init__(self, spreadsheet_id):
        self.service = Creds.get_service()
        self.spreadsheet_id = spreadsheet_id

    def clear_spreadsheet(self):
        sheet_id_list = self.get_sheet_id_list()

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
                                "title": "UNIT TEST {}".format(time.time()),
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
        self.spreadsheet_id = Constants.unit_test_spreadsheet_id
        self.sheet_name = 'UNIT TEST'
        self.util = ClientTestUtils(self.spreadsheet_id)
        self.util.clear_spreadsheet()

    def test_constructor(self):
        client = Client(spreadsheet_id=Constants.unit_test_spreadsheet_id, sheet_name=Constants.unit_test_sheet_name)
        expected_service = Creds.get_service()
        self.assertEqual(Constants.unit_test_spreadsheet_id, client._spreadsheet_id)
        self.assertEqual(Constants.unit_test_sheet_name, client._sheet_name)
        self.assertEqual(expected_service.__class__.__name__, client._service.__class__.__name__)

    def test_set_cell(self):
        client = Client(spreadsheet_id=self.spreadsheet_id, sheet_name=self.sheet_name)
        sheet_range = 'A1:B2'
        exp_values = [[Cell("foo"), Cell("bar")], [Cell("baz")]]

        client.set(sheet_range, exp_values)

        values = self.util.read_cell('A1:B2')

        for i, row in enumerate(values):
            self.assertCountEqual(exp_values[i], row)

    def test__get_sheet_id(self):
        client = Client(spreadsheet_id=self.spreadsheet_id, sheet_name=self.sheet_name)
        self.assertTrue(isinstance(client._get_sheet_id(), int))

    def test__extract_cell_plain(self):
        value_field_pairs = [["a string", "stringValue"], [0, "numberValue"]]
        for exp_value, value_field_name in value_field_pairs:
            plain_cell = Cell(exp_value)
            cell_json, update_fields = Client._extract_cell(plain_cell)
            expected_fields = ["userEnteredValue", "effectiveValue"]
            for field in expected_fields:
                self.assertTrue(field in cell_json)
                self.assertEqual(exp_value, cell_json[field][value_field_name])

            expected_update_fields = "effectiveValue.{},userEnteredValue.{}".format(
                value_field_name,
                value_field_name
            )
            self.assertEqual(expected_update_fields, update_fields)

    def test__extract_cell_formatted(self):
        value = "a string"
        color = {
            "red": 0.1234,
            "blue": 0.5678,
            "green": 0.0
        }
        is_bold = True
        formatted_Cell = FormattedCell("a string", color, is_bold)
        expected_fields = ["userEnteredValue", "effectiveValue", "userEnteredFormat", "effectiveFormat"]
        cell_json, update_fields = Client._extract_cell(formatted_Cell)
        for field in expected_fields:
            self.assertTrue(field in cell_json)
        self.assertEqual(value, cell_json['effectiveValue']['stringValue'])
        self.assertEqual(color, cell_json['effectiveFormat']['backgroundColor'])
        self.assertEqual(is_bold, cell_json['userEnteredFormat']['textFormat']['bold'])

        expected_update_fields = "effectiveValue.stringValue,userEnteredValue.stringValue," +\
                                 "effectiveFormat.backgroundColor,userEnteredFormat.backgroundColor," +\
                                 "effectiveFormat.textFormat.bold,userEnteredFormat.textFormat.bold"
        self.assertEqual(expected_update_fields, update_fields)


if __name__ == '__main__':
    unittest.main()
