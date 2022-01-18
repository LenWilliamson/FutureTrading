import os
import sys
import pandas as pd
from typing import List, Final

from util.lib.DataTransformer import DataTransformer


def store_data_in_chunks(source_path: str, column_names: List[int], chunk_size: Final[int], path: str) -> int:
    chunk_no: int = 0
    for chunk in pd.read_csv(source_path, sep=',', names=column_names, chunksize=chunk_size):
        dt: DataTransformer = DataTransformer(chunk)
        dt.save_data(path, chunk_no)
        chunk_no += 1  # increment chunk number by one
    return 0


def main():
    # Display current working direcotry
    pwd: str = os.getcwd()
    print(f'Print working directory {pwd}')

    if os.name == 'posix':
        # On Unix system the data is found in the directory AggTrades
        ohlc_trades_data: str = pwd + '/OHLC/BTCUSDT-1d-2021-01.csv'
        ohlc_column_names: List[str] = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime',
                                        'QuoteAssetVol', 'NumberOfTrades', 'TakerBuyBaseAssetVol',
                                        'TakerBuyQuoteAssetVol', 'Ignore']
        df = pd.read_csv(ohlc_trades_data, sep=',', names=ohlc_column_names)
        # Get a tweak of our data
        print(df.info())

        # Process aggregated Trades data
        agg_trades_data_path: str = pwd + '/AggTrades/BTCUSDT-aggTrades-2021-01.csv'
        # Initialize pandas dataframe in chucks as size is too large (> 5GB)
        agg_trades_column_names: List[str] = ['AggTradeId', 'Price', 'Quantity', 'FirstTradeId',
                                              'LastTradeId', 'Timestamp', 'Buyer=Maker', 'BestTradPriceMatch']
        chunk_size: Final[int] = 1000000
        root_path: str = pwd
        path: str = os.path.join(root_path, 'AggTrades/DataChunks/BTCUSDT-aggTrades-2021-01')
        store_data_in_chunks(agg_trades_data_path, agg_trades_column_names, chunk_size, path)
        return 0

    elif os.name == 'nt':
        print("You are not working on a Windows machine.")
        return 0
    else:
        print("Only Linus and Windows systems are currently supported.")
        return 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sys.exit(main())

# See Pandas Intro for quick info https://github.com/efldatascience/ds-courses
