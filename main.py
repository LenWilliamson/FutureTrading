import os
import pandas as pd


def main():
    # Display current working direcotry
    pwd = os.getcwd()
    print(f'Print working directory {pwd}')

    if os.name == 'posix':
        # On Unix system the data is found in the directory AggTrades
        agg_trades_data = pwd + '/AggTrades/BTCUSDT-aggTrades-2021-01.csv'
        ohlc_trades_data = pwd + '/OHLC/BTCUSDT-1d-2021-01.csv'

        # Initialize pandas dataframe in chucks as size is too large (> 5GB)
        agg_column_names = ['AggTradeId', 'Price', 'Quantity', 'FirstTradeId', 'LastTradeId', 'Timestamp', 'Buyer=Maker',
                        'BestTradPriceMatch']
        ohlc_column_names = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime',
                            'QuoteAssetVol', 'NumberOfTrades', 'TakerBuyBaseAssetVol', 'TakerBuyQuoteAssetVol', 'Ignore']
        agg_nrows = 200

        df_agg_trades = pd.read_csv(agg_trades_data, sep=',', names=agg_column_names, nrows=agg_nrows)
        df_ohlc_trades = pd.read_csv(ohlc_trades_data, sep=',', names=ohlc_column_names)

        # Get a tweak of our data
        print(df_agg_trades.info())
        print(df_ohlc_trades.info())
    elif os.name == 'nt':
        print("You are not working on a Windows machine.")
    else:
        print("Only Linus and Windows systems are currently supported.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See Pandas Intro for quick infos https://github.com/efldatascience/ds-courses
