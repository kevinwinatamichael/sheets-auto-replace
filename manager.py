from typing import List

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
        current_review_sheet = review_client.get('{}!{}'.format(review_client.sheet_name, review_range))
        current_keyword_sheet = keyword_client.get('{}!{}'.format(keyword_client.sheet_name, keyword_range))

        indices_to_replace = Manager.get_indices_to_replace(current_review_sheet)
        # keyword_terms, keyword_indices = Manager.get_keyword_replacement(current_keyword_sheet)

    @staticmethod
    def get_indices_to_replace(current_review_sheet: List[List[FormattedCell]]) -> List[int]:
        indices = []
        for index, row in enumerate(current_review_sheet):
            cell = row[0]
            if cell.bgColor != {"red": 1, "blue": 1, "green": 1}:
                indices.append(index)
        return indices
