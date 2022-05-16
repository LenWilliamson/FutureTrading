from typing import List, Dict
from unittest import TestCase

import datetime as dt

from util.lib.timeConverter import date_time_generator, time_converter


class Test(TestCase):
    class TestTimeConverter(TestCase):
        def test_time_converter(self) -> None:
            self.assertEqual('2022-01-15_23:40:00', time_converter(1642286400019 / 1000))
            self.assertEqual('2022-01-15_23:40:01', time_converter(1642286401019 / 1000))
            self.assertEqual('2022-01-15_23:41:00', time_converter((1642286400019 + (60 * 1000)) / 1000))
            self.assertEqual('2021-01-01_01:00:00', time_converter(1609459200058 / 1000))
            self.assertEqual('2021-01-27_15:02:01', time_converter(1611756121462 / 1000))
            self.assertEqual('2021-02-01_00:59:59', time_converter(1612137599983 / 1000))

    def test_date_time_generator(self):
        start: dt.datetime = dt.datetime(2022,1,1)
        end: dt.datetime = dt.datetime(2022,1,31)
        interval: Dict[str, int] = {'days': 1}
        delta: dt.timedelta = dt.timedelta(**interval)

        target: List[dt.datetime] = [dt.datetime(2022, 1, i + 1) for i in range(31)]

        self.assertEqual(True, target == list(date_time_generator(start=start, end=end, delta=delta)))
