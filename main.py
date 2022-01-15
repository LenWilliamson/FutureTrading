import os
import pandas as pd


def main():
    # Display current working direcotry
    pwd = os.getcwd()
    print(f'Print working directory {pwd}')

    if os.name == 'posix':
        # On Unix system the data is found in the directory AggTrades
        agg_trades_data = pwd + '/AggTrades/BTCUSDT-aggTrades-2021-01.csv'

        # Initialize pandas dataframe in chucks as size is too large (> 5GB)
        column_names = ['AggTradeId', 'Price', 'Quantity', 'FirstTradeId', 'LastTradeId', 'Timestamp', 'Buyer=Maker',
                        'BestTradPriceMatch']
        nrows = 200

        df = pd.read_csv(agg_trades_data, sep=',', names=column_names, nrows=nrows)

        # Get a tweak of our data
        print(df.info())
    elif os.name == 'nt':
        print("You are not working on a Windows machine.")
    else:
        print("Only Linus and Windows systems are currently supported.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
