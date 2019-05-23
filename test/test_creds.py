import os
import time
import unittest

import settings
from creds import Creds


class CredsTestCases(unittest.TestCase):
    pickle_path = os.path.join(settings.ROOT_DIR, "token.pickle")

    def test_get_service_by_time_taken(self):
        if os.path.exists(self.pickle_path):
            os.remove(self.pickle_path)

        start_time = time.time()
        service = Creds.get_service()
        end_time = time.time()

        self.assertTrue((end_time-start_time) >= 1)
        self.assertEqual('Resource', service.__class__.__name__)

        start_time = time.time()
        service = Creds.get_service()
        end_time = time.time()
        self.assertFalse((end_time-start_time) >= 1)
        self.assertEqual('Resource', service.__class__.__name__)


if __name__ == '__main__':
    unittest.main()
