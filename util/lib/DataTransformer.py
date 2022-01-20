import os

class DataTransformer:
    def __init__(self, data_frame):
        self.df = data_frame

    def aggregate_data_to_seconds(self) -> None:
        """
        Aggregates the 'aggTrades' trading data to volume at price
        :return: None
        """

        # 1. Sort data frame by price: lowest -> highest
        # 2. Sum volume for equal price
        # 3. Store data frame

        # 4. Merge all data frames by price and accumulate volume
        # 5. Make Sure data is within January 2021
        # 6. Write Unittest

        return

    def save_data(self, path: str, chunk_no: int) -> None:
        """
        Stores the data in smaller chunks
        :param path: path where data should be stored
        :param chunk_no: chunk number
        :return: NONE
        """
        file_name: str = 'chunk' + str(chunk_no) + '.csv'
        self.df.to_csv(os.path.join(path, file_name), index=False)
        return
