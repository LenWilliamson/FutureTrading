import os
import sys
from typing import List, Final
import pandas as pd
from util.lib.VolumeProfileGenerator import VolumeProfileGenerator

def main():
    # Set working directory to the directory containing the script that was used to invoke the Python interpreter
    os.chdir(sys.path[0])
    # Display current working directory
    pwd: str = os.getcwd()
    print(f'Print working directory {pwd}')

    # The data is found in the directory data
    ohlc_trades_data: str = os.path.join(pwd, 'data', 'ohlc', 'BTCUSDT-1d-2021-01.csv')
    ohlc_column_names: List[str] = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime',
                                    'QuoteAssetVol', 'NumberOfTrades', 'TakerBuyBaseAssetVol',
                                    'TakerBuyQuoteAssetVol', 'Ignore']
    df = pd.read_csv(ohlc_trades_data, sep=',', names=ohlc_column_names)
    # print(df.info())

    # Process aggregated trades data
    agg_trades_data_path: str = os.path.join(pwd, 'data', 'aggTrades', 'BTCUSDT-aggTrades-2021-01.csv')
    # Initialize pandas dataframe in chucks as size is too large (> 5GB)
    agg_trades_column_names: List[str] = ['AggTradeId', 'Price', 'Quantity', 'FirstTradeId',
                                          'LastTradeId', 'Timestamp', 'Buyer=Maker', 'BestTradPriceMatch']
    chunk_size: Final[int] = 1000000
    vpg: VolumeProfileGenerator = VolumeProfileGenerator(agg_trades_data_path,agg_trades_column_names, chunk_size, os.path.join(pwd, 'data', 'volumeProfile'), 'result.csv')
    vpg.generate_volume_profile()
    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sys.exit(main())

# See Pandas Intro for quick info https://github.com/efldatascience/ds-courses
