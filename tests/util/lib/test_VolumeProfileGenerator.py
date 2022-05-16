import filecmp
import os
import datetime as dt
import dataConfig as cfg
from typing import List, Final, Tuple
from unittest import TestCase
from util.lib.VolumeProfileGenerator import VolumeProfileGenerator
from util.lib.fileStorage import create_filename


class TestVolumeProfileGenerator(TestCase):
    chunk_size: Final[int] = 7

    @classmethod
    def setUpClass(cls) -> None:
        print('setUpClass')
        cls.vpg: VolumeProfileGenerator = VolumeProfileGenerator(cfg.tAGTR_DP, cfg.AGTR_CNL, cls.chunk_size, cfg.tVOLP_DP)

    # def _setUp(self) -> None:
    #     print('_setUp')

    # def tearDown(self) -> None:
    #     print('tearDown')

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     print('tearDownClass')

    def test_gen_volume_profile(self):
        src: str = 'td1.csv'
        out: str = 'test_td1.csv'
        self.vpg.gen_volume_profile(src_file_name=src, dst_file_name=out)
        target: str = os.path.join(cfg.tVOLP_DP, src)
        test: str = os.path.join(cfg.tVOLP_DP, out)
        self.assertEqual(True, filecmp.cmp(test, target, shallow=True))

    def test_gen_volume_profile_interval(self):
        list_of_time_stamps: List[Tuple[dt.datetime, dt.datetime]] = \
            [(dt.datetime(2021, 1, 1, 1), dt.datetime(2021, 1, 1, 1, 59, 59, 10 ** 6 - 1)),
             (dt.datetime(2021, 1, 1, 2), dt.datetime(2021, 1, 1, 2, 59, 59, 10 ** 6 - 1)),
             (dt.datetime(2021, 1, 1, 3), dt.datetime(2021, 1, 1, 3, 59, 59, 10 ** 6 - 1)),
             (dt.datetime(2021, 1, 1, 4), dt.datetime(2021, 1, 1, 4, 59, 59, 10 ** 6 - 1)),
             (dt.datetime(2021, 1, 1, 5), dt.datetime(2021, 1, 1, 5, 59, 59, 10 ** 6 - 1)),
             (dt.datetime(2021, 1, 1, 1), dt.datetime(2021, 1, 1, 2, 59, 59, 10 ** 6 - 1)),
             (dt.datetime(2021, 1, 1, 1), dt.datetime(2021, 1, 1, 5, 59, 59, 10 ** 6 - 1))]
        src: str = 'td1_interval.csv'
        out: str = 'test_' + src
        for dt_start, dt_end in list_of_time_stamps:
            self.vpg.gen_volume_profile_interval(
                src_file=src,
                dst_file=out,
                start_time=dt_start.timestamp(),
                end_time=dt_end.timestamp()
            )
            src_target: str = create_filename(t=(dt_start, dt_end), file=src)
            target: str = os.path.join(cfg.tVOLP_DP, src_target)
            test: str = os.path.join(cfg.tVOLP_DP, 'test_' + src_target)
            with self.subTest(msg=test):
                self.assertEqual(True, filecmp.cmp(test, target, shallow=True))

        # TestDataStorage Exception
        lower: dt.datetime = dt.datetime(1990, 1, 1)
        upper: dt.datetime = dt.datetime(1990, 1, 2)
        self.assertRaises(
            ValueError,
            self.vpg.gen_volume_profile_interval,
            src_file=src,
            dst_file=out,
            start_time=lower.timestamp(),
            end_time=upper.timestamp()
        )
