import os
import time
import unittest

import settings
from creds import Creds


class CredsTestCases(unittest.TestCase):
    pickle_path = os.path.join(settings.ROOT_DIR, "token.pickle")

    def test_get_creds_by_timing(self):
        if os.path.exists(self.pickle_path):
            os.remove(self.pickle_path)

        start_time = time.time()
        creds = Creds.get_creds()
        end_time = time.time()

        self.assertTrue((end_time- start_time) >= 1)
        self.assertTrue(creds.valid)
        self.assertEqual('Credentials', creds.__class__.__name__)

        start_time = time.time()
        creds = Creds.get_creds()
        end_time = time.time()
        self.assertFalse((end_time - start_time) >= 1)
        self.assertTrue(creds.valid)
        self.assertEqual('Credentials', creds.__class__.__name__)


if __name__ == '__main__':
    unittest.main()
