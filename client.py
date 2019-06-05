import re
import warnings

from cell import Cell
from creds import Creds
from typing import List

from formatted_cell import FormattedCell


class Client:

    def __init__(self, spreadsheet_id=None, sheet_name=None):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self._service = Creds.get_service()
        self._sheet_id = self._get_sheet_id()

    def _get_sheet_id(self):
        request = self._service.spreadsheets().get(spreadsheetId=self.spreadsheet_id)
        spreadsheet = request.execute()
        for sheet in spreadsheet['sheets']:
            name = sheet['properties']['title']
            if name == self.sheet_name:
                return sheet['properties']['sheetId']
            elif name.startswith(self.sheet_name):
                warnings.warn("prefix is used instead of exact match: {} of {}".format(name, self.sheet_name),
                              UserWarning,
                              stacklevel=1)
                return sheet['properties']['sheetId']
        raise KeyError("sheet with sheet name {} not found".format(self.sheet_name))

    @staticmethod
    def _parse_range(range_):
        if not re.match(r"[a-zA-Z]+[0-9]*:[a-zA-Z]+[0-9]*", range_):
            raise ValueError("Invalid range")
        start, stop = range_.split(':')
        start_col_len = re.match(r"[a-zA-Z]+", start).end()
        start_column = start[:start_col_len]
        start_row = start[start_col_len:]

        column_index = 0
        for index, c in enumerate(start_column.upper()):
            column_index += 26**(len(start_column)-index-1) * (ord(c) - ord('A') + 1)
        column_index -= 1

        row_index = int(start_row)-1 if start_row else 0

        return row_index, column_index

    def set(self, range_: str, values: List[List[Cell]]) -> None:
        row_index, column_index = Client._parse_range(range_)
        requests = []
        for row_offset, row in enumerate(values):
            for column_offset, col in enumerate(row):
                cell = values[row_offset][column_offset]
                cell_json, update_fields = Client._extract_cell(cell)
                requests.append(
                    self._format_json_request(cell_json, update_fields, row_index, row_offset, column_index,
                                              column_offset)
                )
        if requests:
            self._service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=
            {
                'requests': requests
            }).execute()

    @staticmethod
    def _extract_cell(cell: Cell) -> object:
        if isinstance(cell.value, str):
            cell_value_json = {
                'stringValue': cell.value,
            }
            update_fields = 'effectiveValue.stringValue,userEnteredValue.stringValue'
        elif isinstance(cell.value, int):
            cell_value_json = {
                'numberValue': cell.value,
            }
            update_fields = 'effectiveValue.numberValue,userEnteredValue.numberValue'
        else:
            raise TypeError("Not supported cell type")

        cell_json = {
            "effectiveValue": cell_value_json,
            "userEnteredValue": cell_value_json,
        }

        if isinstance(cell, FormattedCell):
            cell_format_json = {
                "backgroundColor": cell.bgColor,
                "textFormat": {"bold": cell.bold},
            }
            cell_json['effectiveFormat'] = cell_format_json
            cell_json['userEnteredFormat'] = cell_format_json

            update_fields += ',effectiveFormat.backgroundColor,userEnteredFormat.backgroundColor,' +\
                             'effectiveFormat.textFormat.bold,userEnteredFormat.textFormat.bold'
        return cell_json, update_fields

    def _format_json_request(self, cell_json, update_fields, row_index, row_offset, column_index, column_offset):
        return {
            'updateCells': {
                'rows': {
                    'values': [
                        cell_json,
                    ]
                },
                'fields': update_fields,
                'start': {
                    "sheetId": self._sheet_id,
                    "rowIndex": row_index + row_offset,
                    "columnIndex": column_index + column_offset,
                }
            }
        }

    def get(self, range_: str) -> List[List[Cell]]:
        request = self._service.spreadsheets().get(spreadsheetId=self.spreadsheet_id,
                                                   ranges=[range_],
                                                   includeGridData=True)
        response = request.execute()
        rows = response['sheets'][0]['data'][0]['rowData']
        cell_data = []
        for row in rows:
            cell_row = []
            for cell in row['values']:
                if 'stringValue' in cell['effectiveValue']:
                    cell_value = cell['effectiveValue']['stringValue']
                elif 'numberValue' in cell['effectiveValue']:
                    cell_value = cell['effectiveValue']['numberValue']
                else:
                    raise KeyError("stringValue and numberValue not found in cell['effectiveValue']")

                cell_row.append(FormattedCell(
                    cell_value,
                    cell['effectiveFormat']['backgroundColor'],
                    cell['effectiveFormat']['textFormat']['bold']
                ))
        return cell_data
