import os
import pandas as pd
from typing import List, Final


class VolumeProfileGenerator:
    def __init__(self, data_source: str, column_names: List[str], chunk_size: Final[int], destination_path: str, file_name: str) -> None:
        self.ds: str = data_source
        self.cn: List[str] = column_names
        self.cs: Final[int] = chunk_size
        self.dp: str = destination_path
        self.fn: str = file_name

    def generate_volume_profile(self) -> None:
        list_of_df: List[pd.DataFrame] = []
        for chunk in pd.read_csv(filepath_or_buffer=self.ds, sep=',', names=self.cn, chunksize=self.cs):
            # Step1: Summarize price information
            chunk['Price'] = chunk['Price'].map(round)
            # Step2: Sort by price
            chunk.sort_values(by=['Price'], inplace=True)
            # Step3: Accumulate volumes by price and append to list of dataframes
            #        The data frame is collapsed from self.cn to ['Price', 'Quantity']
            list_of_df.append(chunk.groupby(['Price'])['Quantity'].sum().reset_index())

        # Step4: Merge volume data
        merged: pd.DataFrame = self._merge_volume_data(list_of_df)
        # Step5: Store volume data
        self._save_data(merged, file_name=self.fn)

    def _merge_volume_data(self, lodf: List[pd.DataFrame], n: int = 5) -> pd.DataFrame:
        """
        Recursively merge list of pandas data frames until the list only got one final data frame.
        The merge is based on quantity and price.
        :param lodf: list of data frames with columns = ['Price', 'Quantity']
        :return: merged data frame by quantity
        """
        if not lodf:
            # Empty list
            return lodf
        elif len(lodf) < 5:
            return pd.concat(lodf).groupby(['Price']).sum().reset_index()
        else:
            # Only merge five elements at time
            buffer = [x for _, x in zip(range(n), lodf)]
            # Remove buffer from list of data frames
            lodf = lodf[n:]
            # Merge data frames
            merged = pd.concat(buffer).groupby(['Price']).sum().reset_index()
            # Insert merged data frame as new head element of the list
            lodf.insert(0, merged)
            return self._merge_volume_data(lodf)

    def _save_data(self, df: pd.DataFrame, file_name: str) -> None:
        df.to_csv(os.path.join(self.dp, file_name), index=False)


