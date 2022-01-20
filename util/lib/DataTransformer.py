import os

class DataTransformer:
    def __init__(self, data_frame):
        self.df = data_frame

    def sort_by_price(self) -> None:
        """
        Sorts data frame by price
        :return: None
        """
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


    # 1. Sort data frame by price: lowest -> highest
    # 2. Sum volume for equal price
    # 3. Store data frame

    # 4. Merge all data chunks by price and accumulate volume
    # 5. Write Unittest