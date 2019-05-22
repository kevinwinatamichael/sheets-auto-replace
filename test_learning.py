import os
import pickle
import unittest
from pprint import pprint

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'


class LearningTest(unittest.TestCase):
    def setUp(self):
        self.service = build('sheets', 'v4', credentials=LearningTest.get_creds())
        self.spreadsheet_id = '1VYgGx0bvtWnmR9mpTh1i5nZT652vnevdx0ibNXX_8DQ'

    @staticmethod
    def get_creds():
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def test_quick_start(self):
        service = self.service

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('Name, Major:')
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print('%s, %s' % (row[0], row[4]))

        self.assertTrue(True)

    @unittest.skip
    def test_create_sheet(self):
        title = 'test_title'
        service = self.service
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId').execute()
        print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))

    def test_read_value(self):
        service = self.service
        range_ = 'A1:B3'

        value_render_option = 'FORMATTED_VALUE'
        date_time_render_option = 'SERIAL_NUMBER'
        request = service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=range_,
                                                      valueRenderOption=value_render_option,
                                                      dateTimeRenderOption=date_time_render_option)
        response = request.execute()
        pprint(response)

    def test_write(self):
        values = [
            [
                'Kambing', '=1+2'
            ],
            [
                'kucing'
            ]
        ]
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id, range='B7:C9',
            valueInputOption="USER_ENTERED", body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))


if __name__ == '__main__':
    unittest.main()
