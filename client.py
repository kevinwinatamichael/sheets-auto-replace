from creds import Creds


class Client:
    def __init__(self, sheet_id=None, sheet_name=None):
        self._sheet_id = sheet_id
        self._sheet_name = sheet_name
        self._service = Creds.get_service()

