from unittest import TestCase
from util.lib.timeConverter import  time_converter


class TestTimeConverter(TestCase):
    def test_time_converter(self) -> None:
        self.assertEqual('2022-01-15_23:40:00', time_converter(1642286400019 / 1000))
        self.assertEqual('2022-01-15_23:40:01', time_converter(1642286401019 / 1000))
        self.assertEqual('2022-01-15_23:41:00', time_converter((1642286400019 + (60 * 1000)) / 1000))
        self.assertEqual('2021-01-01_01:00:00', time_converter(1609459200058 / 1000))
        self.assertEqual('2021-01-27_15:02:01', time_converter(1611756121462 / 1000))
        self.assertEqual('2021-02-01_00:59:59', time_converter(1612137599983 / 1000))

