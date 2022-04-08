import os
from functools import partial
from typing import List, Final, Callable, Any

import pandas as pd
import dataConfig as cfg
from util.functionalLib.functional import foldl


def _in_time_interval(row: pd.DataFrame, start_time: int, end_time: int) -> bool:
    """
    Checks if the timestamp of the current row is in the given interval
    :param row: Current row of the data frame
    :param start_time: posix start time
    :param end_time: posix end time
    :return: True if condition is met
    """
    return start_time <= row[cfg.AGTR_CN['ts']] <= end_time


def _volume_per_tick(acc: List[pd.DataFrame], chunk: pd.DataFrame, predicate: Callable[[Any], bool] = None):
    """
    Computes the traded volume per price tick per unit.
    Example: Unit = USDT => 4000.5USDT are summarized to 4001USDT and so on
    :param acc: Resulting list of data frames with volume per tick
    :param chunk: Data frame to process
    :param predicate: If set, one can filter the data frame
    :return: acc
    """
    if predicate:
        chunk['in_interval'] = chunk.apply(predicate, axis=1)
        chunk = chunk.drop(chunk[~chunk['in_interval']].index)
    if chunk.empty:
        return acc
    else:
        # Summarize price information
        chunk[cfg.AGTR_CN['px']] = chunk[cfg.AGTR_CN['px']].map(round)
        # Sort by price
        chunk.sort_values(by=[cfg.AGTR_CN['px']], inplace=True)
        # Accumulate volumes by price and append to list of dataframes
        # The data frame is collapsed from self.cn to ['Price', 'Quantity']
        return acc + [chunk.groupby([cfg.AGTR_CN['px']])[cfg.AGTR_CN['qx']].sum().reset_index()]


class VolumeProfileGenerator:
    def __init__(self, data_source: str, column_names: List[str], chunk_size: int, destination_path: str) -> None:
        self.ds: Final[str] = data_source
        self.cn: Final[List[str]] = column_names
        self.cs: Final[int] = chunk_size
        self.dp: Final[str] = destination_path

    def gen_volume_profile(self, src_file_name: str, dst_file_name: str) -> None:
        """
        Generates volume profile for given time interval and saves the data
        :param src_file_name: Name of the source file
        :param dst_file_name: Name of the destination file where the result is stored
        :return: None/Void
        """
        acc: List[pd.DataFrame] = foldl(
            f=_volume_per_tick,
            acc=[],
            xs=pd.read_csv(
                filepath_or_buffer=os.path.join(self.ds, src_file_name),
                sep=',',
                names=self.cn,
                chunksize=self.cs
            )
        )
        # Merge volume data
        head, *tail = acc
        if tail:
            merged = head.append(tail, ignore_index=True)
            grouped = merged.groupby([cfg.AGTR_CN['px']]).sum().reset_index()
        else:
            grouped = head.groupby([cfg.AGTR_CN['px']]).sum().reset_index()
        # Save volume data to file
        self._save_data(grouped, file_name=dst_file_name)

    def gen_volume_profile_interval(self, src_file: str, dst_file: str, start_time: int, end_time: int) -> None:
        """
        Generates volume profile for given time interval and saves the data
        :param dst_file: Name of the source file
        :param src_file: Name of the destination file where the result is stored
        :param start_time: Posix time stamp in milliseconds
        :param end_time: Posix time stamp in milliseconds
        :return: None/Void
        """
        pred: Callable[[pd.DataFrame], bool] = partial(_in_time_interval, start_time=start_time, end_time=end_time)
        func: partial[List[pd.DataFrame], pd.DataFrame] = partial(_volume_per_tick, predicate=pred)
        acc: List[pd.DataFrame] = foldl(
            f=func,
            acc=[],
            xs=pd.read_csv(
                filepath_or_buffer=os.path.join(self.ds, src_file),
                sep=',',
                names=self.cn,
                chunksize=self.cs
            )
        )
        if acc:
            # Merge volume data
            head, *tail = acc
            if tail:
                merged = head.append(tail, ignore_index=True)
                grouped = merged.groupby([cfg.AGTR_CN['px']]).sum().reset_index()
            else:
                grouped = head.groupby([cfg.AGTR_CN['px']]).sum().reset_index()
            # Save volume data to file
            self._save_data(grouped, file_name=dst_file)
        else:
            print(f'start time: {start_time} and end time: {end_time} are out of range.')

    def _save_data(self, df: pd.DataFrame, file_name: str) -> None:
        df.to_csv(os.path.join(self.dp, file_name), index=False)
