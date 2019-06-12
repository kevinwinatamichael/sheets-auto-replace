import re
import time
from typing import List, Tuple

from cell import Cell
from client import Client
from formatted_cell import FormattedCell
from parser import A1Parser


class Manager:

    @staticmethod
    def main(args):
        review_client = Client(args['reviewSheetId'], args['reviewSheetName'])
        keyword_client = Client(args['keywordSheetId'], args['keywordSheetName'])
        review_range = args['reviewRange']
        keyword_range = args['keywordRange']

        Manager._validate_range_width(review_range, 1, "Review Range Width must be one")
        Manager._validate_range_width(keyword_range, 2, "Keyword Range width must be two")

        while True:
            Manager.perform(review_client, keyword_client, review_range, keyword_range)
            time.sleep(5)

    @staticmethod
    def _validate_range_width(range_, width, error_msg="Invalid Range Width"):
        A1Parser.validate_range(range_)
        start, stop = A1Parser.split_range(range_)
        __, start_col = A1Parser.parse_cell(start)
        __, stop_col = A1Parser.parse_cell(stop)
        if start_col+(width-1) != stop_col:
            raise ValueError(error_msg)

    @staticmethod
    def perform(review_client, keyword_client, review_range, keyword_range):
        current_review_sheet = review_client.get(review_range)
        current_keyword_sheet = keyword_client.get(keyword_range)

        indices_to_replace = Manager.get_indices_to_replace(current_review_sheet)
        keyword_terms, keyword_indices = Manager.get_keyword_replacement(len(indices_to_replace), current_keyword_sheet)

        if len(indices_to_replace) == 0:
            print("Found nothing on", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            return

        review_start_cell = A1Parser.split_range(review_range)[0]
        review_col = re.sub('[0-9]', '', review_start_cell)
        review_base_row = int(re.sub('[a-zA-Z]', '', review_start_cell))
        for i in range(len(indices_to_replace)):
            review_client.set('{}{}:{}{}'.format(
                review_col,
                indices_to_replace[i]+review_base_row,
                review_col,
                indices_to_replace[i]+review_base_row
            ), [[FormattedCell(keyword_terms[i], {"red": 1, "blue": 1, "green": 1}, True)]])

        keyword_check_col = re.sub('[0-9]', '', A1Parser.split_range(keyword_range)[1])
        keyword_base_row = int(re.sub('[a-zA-Z]', '', A1Parser.split_range(keyword_range)[0]))
        keyword_client.set('{}{}:{}{}'.format(
                keyword_check_col,
                keyword_indices[0]+keyword_base_row,
                keyword_check_col,
                keyword_indices[-1]+keyword_base_row
            ),
            [[Cell(1)]]*len(keyword_indices)
        )
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ': Succesfully replace:', keyword_terms)

    @staticmethod
    def get_indices_to_replace(current_review_sheet: List[List[FormattedCell]]) -> List[int]:
        indices = []
        for index, row in enumerate(current_review_sheet):
            cell = row[0]
            if cell.bgColor != {"red": 1, "blue": 1, "green": 1}:
                indices.append(index)
        return indices

    @staticmethod
    def get_keyword_replacement(number_of_replacement: int, current_keyword_sheet: List[List[FormattedCell]]) -> Tuple[List[str], List[int]]:
        keyword_terms = []
        keyword_indices = []
        for index, row in enumerate(current_keyword_sheet):
            if Manager.this_row_is_checked(row):
                continue
            if number_of_replacement>0:
                keyword_terms.append(row[0].value)
                keyword_indices.append(index)
                number_of_replacement -= 1

        if number_of_replacement > 0:
            raise ValueError("Not enough keyword terms in the range for replacement.")
        return keyword_terms, keyword_indices

    @staticmethod
    def this_row_is_checked(row: List[FormattedCell]) -> bool:
        if len(row) == 2:
            return True
