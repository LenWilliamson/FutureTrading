import datetime
import filecmp
import os
import datetime as dt

from typing import List, Final, Tuple
from unittest import TestCase
from util.lib.VolumeProfileGenerator import VolumeProfileGenerator


class TestVolumeProfileGenerator(TestCase):
    cwd: str = None
    src_data_path: str = None
    dst_data_path: str = None
    agg_trades_column_names: str = None
    chunk_size: Final[int] = 7

    @classmethod
    def setUpClass(cls) -> None:
        print('setUpClass')
        cls.cwd: str = os.getcwd()

        cls.src_data_path: str = os.path.join(cls.cwd, 'testData', 'aggTrades')
        cls.dst_data_path: str = os.path.join(cls.cwd, 'testData', 'volumeProfile')
        cls.agg_trades_column_names: List[str] = ['AggTradeId', 'Price', 'Quantity', 'FirstTradeId',
                                                  'LastTradeId', 'Timestamp', 'Buyer=Maker', 'BestTradPriceMatch']
        cls.vpg: VolumeProfileGenerator = VolumeProfileGenerator(cls.src_data_path, cls.agg_trades_column_names, cls.chunk_size, cls.dst_data_path)

    # def _setUp(self) -> None:
    #     print('_setUp')

    # def tearDown(self) -> None:
    #     print('tearDown')

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     print('tearDownClass')

    def test_generate_volume_profile(self):
        src: str = 'td1.csv'
        out: str = 'test_td1.csv'
        self.vpg.generate_volume_profile(src_file_name=src, dst_file_name=out)
        target: str = os.path.join(self.dst_data_path, src)
        test: str = os.path.join(self.dst_data_path, out)
        self.assertEqual(True, filecmp.cmp(test, target, shallow=True))

    def test_generate_volume_profile_interval(self):
        list_of_time_stamps: List[Tuple[datetime.datetime, datetime.datetime]] = \
            [(dt.datetime(2021, 1, 1, 1), dt.datetime(2021, 1, 1, 1, 59, 59)),
             (dt.datetime(2021, 1, 1, 2), dt.datetime(2021, 1, 1, 2, 59, 59)),
             (dt.datetime(2021, 1, 1, 3), dt.datetime(2021, 1, 1, 3, 59, 59)),
             (dt.datetime(2021, 1, 1, 4), dt.datetime(2021, 1, 1, 4, 59, 59)),
             (dt.datetime(2021, 1, 1, 5), dt.datetime(2021, 1, 1, 5, 59, 59)),
             (dt.datetime(2021, 1, 1, 1), dt.datetime(2021, 1, 1, 2, 59, 59)),
             (dt.datetime(2021, 1, 1, 1), dt.datetime(2021, 1, 1, 5, 59, 59))]
        src: str = 'td1_interval.csv'
        for dt_start, dt_end in list_of_time_stamps:
            start: str = dt_start.strftime("%Y-%m-%d_%H:%M:%S")
            end: str = dt_end.strftime("%Y-%m-%d_%H:%M:%S")
            src_target: str = src + '__' + start + '__' + end
            out: str = 'test_' + src_target
            self.vpg.generate_volume_profile_interval(src_file_name=src, dst_file_name=out, start_time=int(dt_start.timestamp()), end_time=int(dt_end.timestamp()))
            target: str = os.path.join(self.dst_data_path, src_target)
            test: str = os.path.join(self.dst_data_path, out)
            with self.subTest(msg=test):
                self.assertEqual(True, filecmp.cmp(test, target, shallow=True))
