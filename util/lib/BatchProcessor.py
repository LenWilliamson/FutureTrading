import concurrent.futures
import datetime as dt
import os
import sys
from abc import abstractmethod
from functools import partial
from typing import Final, List, Dict, Tuple, Callable
from dateutil.relativedelta import relativedelta

import dataConfig as cfg
from util.lib.VolumeProfileGenerator import VolumeProfileGenerator
from util.lib.timeConverter import time_converter, date_time_generator


class BatchProcessor:
    def __init__(self, batch_dir: str):
        """

        :param batch_dir:
        """
        self.bd_bytes: Final[bytes] = os.fsencode(batch_dir)
        self.bd_str: Final[str] = batch_dir

    @abstractmethod
    def process_batch(self, interval: int, offset: str, test: bool = False) -> None:
        raise NotImplementedError('Subclasses should implement this!')


class VolumeBatchProcessor(BatchProcessor):
    def __init__(self, batch_dir: str, column_names: List[str], chunk_size: int, destination_path: str):
        """

        :param batch_dir:
        :param column_names:
        :param chunk_size:
        :param destination_path:
        """
        BatchProcessor.__init__(self, batch_dir=batch_dir)
        self.vpg: Final[VolumeProfileGenerator] = VolumeProfileGenerator(
            data_source=batch_dir,
            column_names=column_names,
            chunk_size=chunk_size,
            destination_path=destination_path
        )

    def process_batch(self, interval: Dict[str, int], offset: str, test: bool = False) -> None:
        """
        Processes batch of .csv files that contains aggregated trades of exactly one month.
        :param interval: Time interval in hours that should be filtered
            Possible arguments for integer n > 0:
                ['hours',n] = n hours
                ['days',n] = n days
                ['weeks',n] = n week
        :param offset: If we process an aggTrades batch the offset is 'BTCUSDT-aggTrades-'
        :param test: If we call the function from test we prepend 'test_' to filename
        :return: None/Void
        """
        cfg.LOGGER.debug(
            f'{sys.argv[0]} :: CALL :: VolumeBatchProcessor(BatchProcessor).process_batch({interval}, {offset}, {test})')

        filenames = map(
            os.fsdecode,
            filter(
                lambda x: os.fsdecode(filename=x).endswith('.csv'),
                os.listdir(self.bd_bytes)
            )
        )

        f: Callable[[str], None] = partial(self._process_file, interval=interval, offset=offset, test=test)
        for _ in map(f, filenames):
            pass

    def _process_file(self, file: str, interval: Dict[str, int], offset: str, test: bool = False) -> None:
        """
        Processes a single ..csv file that contains aggregated trades of exactly one month.
        :param file: .csv file we want to process
        :param interval: Time interval in hours that should be filtered
            Possible arguments for integer n > 0:
                ['hours',n] = n hours
                ['days',n] = n days
                ['weeks',n] = n week
        :param offset: If we process an aggTrades batch the offset is 'BTCUSDT-aggTrades-'
        :param test: If we call the function from test we prepend 'test_' to filename
        :return: None/Void
        """
        open_dt: dt.datetime = dt.datetime.strptime(file[len(offset):-4], '%Y-%m')
        # Assumption: Aggregated trades data has a relative delta of exactly one month
        end_dt: dt.datetime = open_dt + relativedelta(months=1)
        # Generate list of datetime stamps
        lof_dt: List[dt.datetime] = list(
            date_time_generator(start=open_dt, end=end_dt, delta=dt.timedelta(**interval))
        )

        # Zip list of datetime stamps into tuples of (start, end) datetime objects
        lof_start_end: List[Tuple[dt.datetime, dt.datetime]] = list(zip(lof_dt[:-1], lof_dt[1:]))
        # Number of output files
        n: int = len(lof_start_end)

        args_src_file = [file for _ in range(n)]
        args_dst_file = [out if not test else 'test_' + out for out in args_src_file]
        args_start_time: List[dt.datetime] = [s for s, _ in lof_start_end]
        args_end_time: List[dt.datetime] = [e for _, e in lof_start_end]
        args_sub_dirs: List[List[str]] = [
            [time_converter(time_stamp=open_dt.timestamp()), list(interval.keys())[0]]
            for _ in range(n)
        ]
        args = [
            args_src_file,
            args_dst_file,
            [x.timestamp() for x in args_start_time],
            [x.timestamp() for x in args_end_time],
            args_sub_dirs
        ]

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self.vpg.gen_volume_profile_interval, *args)

