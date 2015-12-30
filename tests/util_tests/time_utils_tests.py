from utils import time_utils
from unittest import TestCase


class TestTimeUtils(TestCase):
    def test_to_utc(self):
        time_in = "2007-04-05T12:30-02:00"
        time_out = time_utils.to_utc(time_in)
        self.assertIsNotNone(time_out)
        self.assertGreater(time_utils.utcnow(), time_out)
        self.assertEqual(time_out.tm_hour, 14)
