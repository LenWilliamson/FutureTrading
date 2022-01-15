from unittest import TestCase
from util.lib.timeConverter import  time_converter

class TestTimeConverter(TestCase):
    def test_time_converter(self):
        self.assertEqual(time_converter(1642286400019), '2022-01-15 23:40:00')
        self.assertEqual(time_converter(1642286401019), '2022-01-15 23:40:01')
        self.assertEqual(time_converter(1642286400019 + (60 * 1000)), '2022-01-15 23:41:00')
