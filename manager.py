from typing import List, Tuple

from client import Client
from formatted_cell import FormattedCell


class Manager:

    @staticmethod
    def main(args):
        review_client = Client(args['reviewSheetId'], args['reviewSheetName'])
        keyword_client = Client(args['keywordSheetId'], args['keywordSheetName'])
        review_range = args['reviewRange']
        keyword_range = args['keywordRange']
        # TODO check review_range width is 1 column
        # TODO check keyword_range width is 2 columns
        while True:
            Manager.perform(review_client, keyword_client, review_range, keyword_range)
            break

    @staticmethod
    def perform(review_client, keyword_client, review_range, keyword_range):
        current_review_sheet = review_client.get(review_range)
        current_keyword_sheet = keyword_client.get(keyword_range)

        indices_to_replace = Manager.get_indices_to_replace(current_review_sheet)
        keyword_terms, keyword_indices = Manager.get_keyword_replacement(len(indices_to_replace), current_keyword_sheet)

        print(indices_to_replace)
        print(keyword_terms, keyword_indices)

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
