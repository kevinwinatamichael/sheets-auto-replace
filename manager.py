from client import Client


class Manager:

    @staticmethod
    def main(args):
        review_client = Client(args['reviewSheetID'], args['reviewSheetName'])
        keyword_client = Client(args['keywordSheetId'], args['keywordSheetName'])
        review_range = args['reviewRange']
        keyword_range = args['keywordRange']
        while True:
            Manager.perform(review_client, keyword_client, review_range, keyword_range)

    @staticmethod
    def perform(review_client, keyword_client, review_range, keyword_range):
        current_review_sheet = review_client.get(review_range)
        current_keyword_sheet = keyword_client.get(keyword_range)
        # TODO process sheets above
