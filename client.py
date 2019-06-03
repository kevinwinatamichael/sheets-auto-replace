import warnings

from cell import Cell
from creds import Creds
from typing import List, Any, Union


class Client:

    def __init__(self, spreadsheet_id=None, sheet_name=None):
        self._spreadsheet_id = spreadsheet_id
        self._sheet_name = sheet_name
        self._service = Creds.get_service()
        self._sheet_id = self._get_sheet_id()

    def _get_sheet_id(self):
        request = self._service.spreadsheets().get(spreadsheetId=self._spreadsheet_id)
        spreadsheet = request.execute()
        for sheet in spreadsheet['sheets']:
            name = sheet['properties']['title']
            if name == self._sheet_name:
                return sheet['properties']['sheetId']
            elif name.startswith(self._sheet_name):
                warnings.warn("prefix is used instead of exact match: {} of {}".format(name, self._sheet_name),
                              UserWarning,
                              stacklevel=1)
                return sheet['properties']['sheetId']
        raise KeyError("sheet with sheet name {} not found".format(self._sheet_name))

    def set(self, range_: str, values: List[List[Cell]]) -> None:
        pass

