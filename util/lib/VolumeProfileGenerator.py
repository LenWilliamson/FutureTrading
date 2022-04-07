import os
import pandas as pd
from typing import List, Final


def _in_time_interval(row: pd.DataFrame, start_time: int, end_time: int) -> bool:
    """
    Checks if the timestamp of the current row is in the given interval
    :param row: Current row of the data frame
    :param start_time: posix start time
    :param end_time: posix end time
    :return: True if condition is met
    """
    return start_time <= row['Timestamp'] <= end_time


class VolumeProfileGenerator:
    def __init__(self, data_source: str, column_names: List[str], chunk_size: Final[int], destination_path: str) -> None:
        self.ds: str = data_source
        self.cn: List[str] = column_names
        self.cs: Final[int] = chunk_size
        self.dp: str = destination_path

    def generate_volume_profile(self, src_file_name: str, dst_file_name: str) -> None:
        """
        Generates volume profile for given time interval and saves the data
        :param src_file_name: Name of the source file
        :param dst_file_name: Name of the destination file where the result is stored
        :return: None/Void
        """
        list_of_df: List[pd.DataFrame] = []
        for chunk in pd.read_csv(filepath_or_buffer=os.path.join(self.ds, src_file_name), sep=',', names=self.cn, chunksize=self.cs):
            # Step1: Summarize price information
            chunk['Price'] = chunk['Price'].map(round)
            # Step2: Sort by price
            chunk.sort_values(by=['Price'], inplace=True)
            # Step3: Accumulate volumes by price and append to list of dataframes
            #        The data frame is collapsed from self.cn to ['Price', 'Quantity']
            list_of_df.append(chunk.groupby(['Price'])['Quantity'].sum().reset_index())

        # Step4: Merge volume data
        head, *tail = list_of_df
        if tail:
            merged = head.append(tail, ignore_index=True)
        grouped = merged.groupby(['Price']).sum().reset_index()
        # Step5: Store volume data
        self._save_data(grouped, file_name=dst_file_name)

    def generate_volume_profile_interval(self, src_file_name: str, dst_file_name: str, start_time: int, end_time: int) -> None:
        """
        Generates volume profile for given time interval and saves the data
        :param dst_file_name: Name of the source file
        :param src_file_name: Name of the destination file where the result is stored
        :param start_time: Posix time stamp in milliseconds
        :param end_time: Posix time stamp in milliseconds
        :return: None/Void
        """
        list_of_df: List[pd.DataFrame] = []
        for chunk in pd.read_csv(filepath_or_buffer=os.path.join(self.ds, src_file_name), sep=',', names=self.cn, chunksize=self.cs):
            # Step1: Flag trades within given time interval with True and drop rest
            chunk['in_interval'] = chunk.apply(_in_time_interval, args=(start_time, end_time), axis=1)
            chunk = chunk.drop(chunk[~chunk['in_interval']].index)
            if chunk.empty:
                # Empty data frame
                continue
            else:
                # Step2: Summarize price information
                chunk['Price'] = chunk['Price'].map(round)
                # Step3: Sort by price
                chunk.sort_values(by=['Price'], inplace=True)
                # Step4: Accumulate volumes by price and append to list of dataframes
                #        The data frame is collapsed from self.cn to ['Price', 'Quantity']
                list_of_df.append(chunk.groupby(['Price'])['Quantity'].sum().reset_index())

        if list_of_df:
            # Step5: Merge volume data
            head, *tail = list_of_df
            if tail:
                merged = head.append(tail, ignore_index=True)
            grouped = merged.groupby(['Price']).sum().reset_index()
            # Step6: Store volume data
            self._save_data(grouped, file_name=dst_file_name)
        else:
            print(f'start time: {start_time} and end time: {end_time} are out of range.')

    def _save_data(self, df: pd.DataFrame, file_name: str) -> None:
        df.to_csv(os.path.join(self.dp, file_name), index=False)


