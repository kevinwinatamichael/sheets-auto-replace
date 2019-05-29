import unittest

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
        ClientTestUtils.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={
                "requests": request
            }
        ).execute()

    def get_sheet_id_list(self):
        response = ClientTestUtils.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        sheets_list = response['sheets']
        sheet_id_list = []
        for sheet in sheets_list:
            sheet_id_list.append(sheet['properties']['sheetId'])
        return sheet_id_list

    def create_new_sheet(self):
        ClientTestUtils.service.spreadsheets().batchUpdate(
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

class ClientTestCases(unittest.TestCase):

    def setUp(self) -> None:
        util = ClientTestUtils(self.spreadhsheet_id)
        util.clear_spreadsheet()
        self.spreadhsheet_id = '1E5AbARR9-wF23aZbsnbnNaz59pGI7-vjmOiiAf7ck5w'

    def test_constructor(self):
        sheet_id = 'dummy_id'
        sheet_name = 'dummy_name'
        client = Client(sheet_id=sheet_id, sheet_name=sheet_name)
        expected_service = Creds.get_service()
        self.assertEqual(sheet_id, client._sheet_id)
        self.assertEqual(sheet_name, client._sheet_name)
        self.assertEqual(expected_service.__class__.__name__, client._service.__class__.__name__)

    def test_set_cell(self):
        pass

if __name__ == '__main__':
    unittest.main()
