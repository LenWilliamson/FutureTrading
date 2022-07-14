# Configuration file for data
import os
import sys
from typing import Final, Dict, List
import logging.config
import datetime as dt

# Set working directory to the directory containing the script that was used to invoke the Python interpreter
# os.chdir(sys.path[0])
# Absolute path of repository
CWD: Final[str] = '/home/len/FutureTrading'
# External Data Source
EDS: Final[str] = '/media/len/ExterneFestplateLenCewa/DataBase'

# Data paths to directories (external drive): /media/len/ExterneFestplateLenCewa/DataBase
OHLC_DP: Final[str] = os.path.join(EDS, 'data', 'ohlc')
AGTR_DP: Final[str] = os.path.join(EDS, 'data', 'aggTrades')
VOLP_DP: Final[str] = os.path.join(EDS, 'data', 'volumeProfile')

# Data paths to test directories
tOHLC_DP: Final[str] = os.path.join(CWD, 'tests', 'testData', 'ohlc')
tAGTR_DP: Final[str] = os.path.join(CWD, 'tests', 'testData', 'aggTrades')
tVOLP_DP: Final[str] = os.path.join(CWD, 'tests', 'testData', 'volumeProfile')

# Data paths to test batch directories
tAGTR_bDP: Final[str] = os.path.join(CWD, 'tests', 'testData', 'batch', 'aggTrades')
tVOLP_bDP: Final[str] = os.path.join(CWD, 'tests', 'testData', 'batch', 'volumeProfile')

# Column names. These list should only be used for initialization of data frames. Use the corresponding dicts
OHLC_CNL: Final[List[str]] = [
    'OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime',
    'QuoteAssetVol', 'NumberOfTrades', 'TakerBuyBaseAssetVol', 'TakerBuyQuoteAssetVol', 'Ignore'
]
AGTR_CNL: Final[List[str]] = [
    'AggTradeId', 'Price', 'Quantity', 'FirstTradeId', 'LastTradeId',
    'Timestamp', 'Buyer=Maker', 'BestTradPriceMatch'
]

# Reference dictionaries
OHLC_CN: Final[Dict[str, str]] = {
    'ots': 'OpenTime',
    'open': 'Open',
    'high': 'High',
    'low': 'Low',
    'close': 'Close',
    'vol': 'Volume',
    'cts': 'CloseTime',
    'qav': 'QuoteAssetVol',
    'not': 'NumberOfTrades',
    'tbbav': 'TakerBuyBaseAssetVol',
    'tbqav': 'TakerBuyQuoteAssetVol',
    'ignore': 'Ignore'
}
AGTR_CN: Final[Dict[str, str]] = {
    'atid': 'AggTradeId',
    'px': 'Price',
    'qx': 'Quantity',
    'ftid': 'FirstTradeId',
    'ltid': 'LastTradeId',
    'ts': 'Timestamp',
    'bm': 'Buyer=Maker',
    'btpm': 'BestTradPriceMatch'
}
VOLP_CN: Final[Dict[str, str]] = {
    'px': 'Price',
    'qx': 'Quantity'
}

# Logging
filename: str = dt.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
logging.config.fileConfig('/home/len/FutureTrading/logFiles/logging.conf', defaults={'logfilename': f'/home/len/FutureTrading/logFiles/logs/{filename}.log'})
LOGGER = logging.getLogger('root')
