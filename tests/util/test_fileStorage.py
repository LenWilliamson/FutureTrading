import os
import shutil
from typing import List, Tuple, Final
from unittest import TestCase
import dataConfig as cfg
import datetime as dt

import pandas as pd

from util.lib.fileStorage import create_filename, save_data


class TestDataStorage(TestCase):
    dst_dir: Final[str] = os.path.join(cfg.CWD, 'tests', 'testDataDirs', 'root')
    file_name: Final[str] = 'td1.csv'

    @classmethod
    def setUpClass(cls) -> None:
        print('setUpClass')
        cls.df: pd.DataFrame = pd.read_csv(
            filepath_or_buffer=os.path.join(cfg.tVOLP_DP, cls.file_name),
            sep=',',
            names=cfg.VOLP_CN
        )
        cls.sub_dirs: List[List[str]] = [
            [''],
            ['subdir1'],
            [os.path.join('subdir1', 'subsubdir1')],
            [os.path.join('subdir1', 'subsubdir2')],
            ['subdir2']
        ]
        cls.target_dirs: List[str] = [
            cls.dst_dir,
            os.path.join(cls.dst_dir, 'subdir1'),
            os.path.join(cls.dst_dir, 'subdir1', 'subsubdir1'),
            os.path.join(cls.dst_dir, 'subdir1', 'subsubdir2'),
            os.path.join(cls.dst_dir, 'subdir2')
        ]
        cls.target_files: List[str] = [
            os.path.join(cls.dst_dir, cls.file_name),
            os.path.join(cls.dst_dir, 'subdir1', cls.file_name),
            os.path.join(cls.dst_dir, 'subdir1', 'subsubdir1', cls.file_name),
            os.path.join(cls.dst_dir, 'subdir1', 'subsubdir2', cls.file_name),
            os.path.join(cls.dst_dir, 'subdir2', cls.file_name)
        ]

        # We want to test all sub directories and the root dir
        cls.num_of_tests = len(cls.sub_dirs)

    @classmethod
    def tearDownClass(cls) -> None:
        print('tearDownClass')
        shutil.rmtree(cls.dst_dir)

    def test_save_data(self) -> None:
        """
        os.path.isfile()
        os.path.exists()
        https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
        :return:
        """

        for i in range(self.num_of_tests):
            with self.subTest(msg=self.target_dirs[i] + f' and /{self.file_name}'):
                save_data(self.df, self.dst_dir, self.file_name, self.sub_dirs[i])
                # Check correct directory structure
                self.assertEqual(True, os.path.exists(self.target_dirs[i]))
                # Check correct file location
                self.assertEqual(True, os.path.isfile(self.target_files[i]))


class TestFilenames(TestCase):
    def test_create_filename(self) -> None:
        file_name: str = 'td1_interval.csv'
        list_of_time_stamps: List[Tuple[dt.datetime, dt.datetime]] = \
            [(dt.datetime(2021, 1, 1, 1), dt.datetime(2021, 1, 1, 1, 59, 59, 10 ** 6 - 1)),
             (dt.datetime(2021, 1, 1, 2), dt.datetime(2021, 1, 1, 2, 59, 59, 10 ** 6 - 1)),
             (dt.datetime(2021, 1, 1, 3), dt.datetime(2021, 1, 1, 3, 59, 59, 10 ** 6 - 1)),
             (dt.datetime(2021, 1, 1, 4), dt.datetime(2021, 1, 1, 4, 59, 59, 10 ** 6 - 1)),
             (dt.datetime(2021, 1, 1, 5), dt.datetime(2021, 1, 1, 5, 59, 59, 10 ** 6 - 1)),
             (dt.datetime(2021, 1, 1, 1), dt.datetime(2021, 1, 1, 2, 59, 59, 10 ** 6 - 1)),
             (dt.datetime(2021, 1, 1, 1), dt.datetime(2021, 1, 1, 5, 59, 59, 10 ** 6 - 1))]

        target_file_extensions: List[str] = \
            ['td1_interval__2021-01-01_01:00:00__2021-01-01_01:59:59.csv',
             'td1_interval__2021-01-01_02:00:00__2021-01-01_02:59:59.csv',
             'td1_interval__2021-01-01_03:00:00__2021-01-01_03:59:59.csv',
             'td1_interval__2021-01-01_04:00:00__2021-01-01_04:59:59.csv',
             'td1_interval__2021-01-01_05:00:00__2021-01-01_05:59:59.csv',
             'td1_interval__2021-01-01_01:00:00__2021-01-01_02:59:59.csv',
             'td1_interval__2021-01-01_01:00:00__2021-01-01_05:59:59.csv']

        for target, ts in zip(target_file_extensions, list_of_time_stamps):
            with self.subTest(msg=target):
                self.assertEqual(target, create_filename(t=ts, file=file_name))
