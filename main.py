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
    # Set working directory to the directory containing the script that was used to invoke the Python interpreter
    os.chdir(sys.path[0])
    # Display current working direcotry
    pwd: str = os.getcwd()
    print(f'Print working directory {pwd}')

    # On Unix system the data is found in the directory aggTrades
    ohlc_trades_data: str = os.path.join(pwd, 'ohlc', 'BTCUSDT-1d-2021-01.csv')
    ohlc_column_names: List[str] = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime',
                                    'QuoteAssetVol', 'NumberOfTrades', 'TakerBuyBaseAssetVol',
                                    'TakerBuyQuoteAssetVol', 'Ignore']
    df = pd.read_csv(ohlc_trades_data, sep=',', names=ohlc_column_names)
    # Get a tweak of our data
    print(df.info())

    # Process aggregated Trades data
    agg_trades_data_path: str = os.path.join(pwd, 'aggTrades', 'BTCUSDT-aggTrades-2021-01.csv')
    # Initialize pandas dataframe in chucks as size is too large (> 5GB)
    agg_trades_column_names: List[str] = ['AggTradeId', 'Price', 'Quantity', 'FirstTradeId',
                                          'LastTradeId', 'Timestamp', 'Buyer=Maker', 'BestTradPriceMatch']
    chunk_size: Final[int] = 1000000
    root_path: str = pwd
    path: str = os.path.join(root_path, 'aggTrades', 'dataChunks', 'BTCUSDT-aggTrades-2021-01')
    # store_data_in_chunks(agg_trades_data_path, agg_trades_column_names, chunk_size, path)
    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sys.exit(main())

# See Pandas Intro for quick info https://github.com/efldatascience/ds-courses
