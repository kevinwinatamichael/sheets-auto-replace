import re


class A1Parser:

    @staticmethod
    def validate_range(range_):
        if not re.match(r"[a-zA-Z]+[0-9]*:[a-zA-Z]+[0-9]*", range_):
            raise ValueError("Invalid range")
        return True

    @staticmethod
    def split_range(range_):
        A1Parser.validate_range(range_)
        start, stop = range_.split(':')
        return start, stop

    @staticmethod
    def parse_cell(cell):
        start_col_len = re.match(r"[a-zA-Z]+", cell).end()
        start_column = cell[:start_col_len]
        start_row = cell[start_col_len:]

        column_index = 0
        for index, c in enumerate(start_column.upper()):
            column_index += 26 ** (len(start_column) - index - 1) * (ord(c) - ord('A') + 1)
        column_index -= 1

        row_index = int(start_row) - 1 if start_row else 0

        return row_index, column_index