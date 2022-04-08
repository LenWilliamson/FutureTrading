from unittest import TestCase
from util.lib.timeConverter import  time_converter


class TestTimeConverter(TestCase):
    def test_time_converter(self) -> None:
        self.assertEqual('2022-01-15 23:40:00', time_converter(1642286400019))
        self.assertEqual('2022-01-15 23:40:01', time_converter(1642286401019))
        self.assertEqual('2022-01-15 23:41:00', time_converter(1642286400019 + (60 * 1000)))
        self.assertEqual('2021-01-01 01:00:00', time_converter(1609459200058))
        self.assertEqual('2021-01-27 15:02:01', time_converter(1611756121462))
        self.assertEqual('2021-02-01 00:59:59', time_converter(1612137599983))

