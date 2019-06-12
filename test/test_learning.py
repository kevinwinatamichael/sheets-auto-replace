import os
import pickle
import unittest
from pprint import pprint

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from creds import Creds
from test.constants import Constants

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'


class LearningTest(unittest.TestCase):
    def setUp(self):
        self.service = Creds.get_service()
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

    def test_ph_search(self):
        service = self.service
        range_ = "'Benchmarking_new'!A2:M4501"

        value_render_option = 'FORMATTED_VALUE'
        date_time_render_option = 'SERIAL_NUMBER'
        request = service.spreadsheets().values().get(spreadsheetId='1AjgnY_4uuwVyLYNHwxnr2UPHd93onAMnOD5veWFER20', range=range_,
                                                      valueRenderOption=value_render_option,
                                                      dateTimeRenderOption=date_time_render_option)
        response = request.execute()
        data1 = response['values']

        from tqdm import tqdm
        d = {}
        for i in tqdm(range(len(data1))):
            try:
                d[data1[i][0]] = data1[i]
            except IndexError:
                d[data1[i][0]] = ["NA"]
        import json

        with open('PH_data.json', 'w') as fp:
            json.dump(d, fp)


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

    def test_append(self):
        values = [
            [
                'Kambingappend', '3 May 2019'
            ],
            [
                'kucing', 'kolak', 'dingin'
            ]
        ]
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id, range='A1:B9',
            valueInputOption='USER_ENTERED', body=body).execute()
        print('{0} cells appended.'.format(result
                                           .get('updates')
                                           .get('updatedCells')))

    def test_search_term(self):
        country = 'SG'

        # BASE_INDEX is EXLUSIVE but TOP_INDEX is INCLUSIVE
        countries = {
            'PH': {
                'review_sheet_name': 'Benchmarking_new',
                'base_index': 5351,
                'top_index': 5601,
                'review_spr_id': '1AjgnY_4uuwVyLYNHwxnr2UPHd93onAMnOD5veWFER20',
                'keyword_spr_id': '1-qFv1b0huGQQeO7YhAdvLlBHlBbeXM-IhJKcgfiCBJo',
                'sheetId': 1357095039,
            },
            'MY': {
                'review_sheet_name': 'Benchmarking_new',
                'base_index': 5201,
                'top_index': 5451,
                'review_spr_id': '15CvH8PBJUktYF46kQypDAd-xvkBP7X37BZiP3uTdX-Y',
                'keyword_spr_id': '1lEX9SzW0HFoekaLBZGpMQrwXcrvCPEninV9u76553Gg',
                'sheetId': 648477030,
            },
            'SG': {
                'review_sheet_name': 'Benchmarking_new',
                'base_index': 5193,
                'top_index': 5443,
                'review_spr_id': '1sS9b6GwZjB0oQ9pvqDOoF-7Qpk3A2c9lyTGNR8hYvKI',
                'keyword_spr_id': '1hExxHZS-OnI4UljbsUYJqi5Vr_VDge3VsR5o2zfDLDw',
                'sheetId': 186606542,
            },
            'TW': {
                'review_sheet_name': 'Benchmarking_new',
                'base_index': 6101,
                'top_index': 6401,
                'review_spr_id': '1bD6BeGpAQxZk99Ai6vMlA0g1ljAZxtYyQ1bDFt7HGLY',
                'keyword_spr_id': '1ul781f5xviUeyt5-YrRk75IrW7cbq7PxPgyvIhBEeNE',
                'sheetId': 222824563,
            },
        }
        review_sheet_name = countries[country]['review_sheet_name']
        base_index = countries[country]['base_index']
        top_index = countries[country]['top_index']
        review_spr_id = countries[country]['review_spr_id']
        keyword_spr_id = countries[country]['keyword_spr_id']
        sheetId = countries[country]['sheetId']

        review_range = "'{}'!A{}:A{}".format(review_sheet_name, base_index, top_index)
        keyword_range = "to-benchmark!A1:B1000"

        request = self.service.spreadsheets().get(spreadsheetId=review_spr_id, ranges=[review_range], includeGridData=True)
        response = request.execute()
        rows = response['sheets'][0]['data'][0]['rowData'][1:]
        review_rows = []
        for row in rows:
            my_row = []
            for value in row['values']:
                color = value['effectiveFormat']['backgroundColor']
                if 'red' not in color:
                    color['red'] = 0
                if 'blue' not in color:
                    color['blue'] = 0
                if 'green' not in color:
                    color['green'] = 0
                if 'effectiveValue' in value:
                    if 'stringValue' in value['effectiveValue']:
                        value_to_append = value['effectiveValue']['stringValue']
                    elif 'numberValue' in value['effectiveValue']:
                        value_to_append = value['effectiveValue']['numberValue']
                    else:
                        raise KeyError('Value not found in effectiveValue.')
                    my_row.append({
                        'value': value_to_append,
                        'colorSum': color['red']+color['blue']+color['green']
                    })
                else:
                    my_row.append({
                        'value': '',
                        'colorSum': color['red']+color['blue']+color['green']
                    })
            review_rows.append(my_row)

        to_replace_index = []
        for i in range(len(review_rows)):
            if review_rows[i][0]['value'] != '' and review_rows[i][0]['colorSum'] != 3:
                to_replace_index.append(i)

        # get the index
        request = self.service.spreadsheets().values().get(spreadsheetId=keyword_spr_id, range=keyword_range)
        response = request.execute()
        keyword_values = response['values'][1:]
        index = None
        for i in range(len(keyword_values)):
            if len(keyword_values[i]) == 1:
                index = i
                break
        new_keywords = []
        for i in range(index, index+len(to_replace_index)):
            new_keywords.append(keyword_values[i][0])
        keywords_to_check_range = "'to-benchmark'!B{}:B{}".format(index+2, index+2+len(to_replace_index))
        values = [[1]]*len(to_replace_index)
        body = {
            'values': values
        }
        checking_keywords_request = self.service.spreadsheets().values().update(
            spreadsheetId=keyword_spr_id, range=keywords_to_check_range,
            valueInputOption="USER_ENTERED", body=body).execute()
        pprint(to_replace_index)
        # replace the keywords
        data = []
        for i in to_replace_index:
            data.append({
                "range": "'{}'!A{}:A{}".format(review_sheet_name, base_index+i+1, base_index+i+1),
                "values": [
                    [new_keywords.pop()]
                ]
            })

        batch_update_values_request_body = {
            'value_input_option': 'RAW',

            'data': data,

        }

        request = self.service.spreadsheets().values().batchUpdate(spreadsheetId=review_spr_id,
                                                              body=batch_update_values_request_body)
        response = request.execute()
        pprint(response)
        cellFormat = {
                            "backgroundColor": {
                                "red": 1,
                                "blue": 1,
                                "green": 1,
                            },
                            "textFormat": {
                                "bold": True
                            }
                        }
        requests = []
        for i in to_replace_index:
            requests.append(
                {
                    'updateCells': {
                        'rows': {
                            'values': [
                                {
                                    "effectiveFormat": cellFormat,
                                    "userEnteredFormat": cellFormat

                                }
                            ]
                        },
                        'fields': 'effectiveFormat.backgroundColor,userEnteredFormat.backgroundColor,\
                                  effectiveFormat.textFormat.bold,userEnteredFormat.textFormat.bold',
                        'start': {
                            "sheetId": sheetId,
                            "rowIndex": (base_index + i),
                            "columnIndex": 0,
                        }
                    }
                }
            )
        response = self.service.spreadsheets().batchUpdate(spreadsheetId=review_spr_id, body=
        {
            'requests': requests
        }).execute()
        pprint(response)

    def test_color(self):
        cellFormat = {
            "backgroundColor": {
                "red": 1,
                "blue": 1,
                "green": 1,
            },
            "textFormat": {
                "bold": True
            }
        }
        requests = []
        requests.append(
            {
                'updateCells': {
                    'rows': {
                        'values': [
                            {
                                "effectiveFormat": cellFormat,
                                "userEnteredFormat": cellFormat

                            }
                        ]
                    },
                    'fields': 'effectiveFormat.backgroundColor,userEnteredFormat.backgroundColor,\
                                      effectiveFormat.textFormat.bold,userEnteredFormat.textFormat.bold',
                    'start': {
                        "sheetId": 2036055998,
                        "rowIndex": 263,
                        "columnIndex": 0,
                    }
                }
            }
        )
        response = self.service.spreadsheets().batchUpdate(spreadsheetId='1LXNphdC92rbOJhA720GGb1BNmAhX20fWIHr-e_fO--Q', body=
        {
            'requests': requests
        }).execute()
        pprint(response)

    def test_get_grid_data(self):
        sheet = self.service.spreadsheets().get(spreadsheetId=Constants.unit_test_spreadsheet_id).execute()
        pprint(sheet['sheets'][0]['properties'])

if __name__ == '__main__':
    unittest.main()
