import csv
import datetime as dt
from util.lib.timeConverter import date_time_generator, time_converter

header = [
    'AggTradeId', 'Price', 'Quantity', 'FirstTradeId', 'LastTradeId',
    'Timestamp', 'Buyer=Maker', 'BestTradPriceMatch'
]
no_test_cases: int = 4
dates_start = [dt.datetime(2000, m + 1, 1) for m in range(no_test_cases)]
dates_end = [dt.datetime(2000, m + 2, 1) for m in range(no_test_cases)]
timedelta = [dt.timedelta(hours=1) for _ in range(4)]

print(dates_start)
print(dates_end)
print(timedelta)

# TODO rewrite in functional manners

# Generate Data
for i in range(no_test_cases):
    data = []
    for e in date_time_generator(start=dates_start[i], end=dates_end[i], delta=timedelta[i]):
        data += [[482561652, 1000 * (i + 1), 1, 536781294, 536781297, time_converter(e.timestamp(), blank=True), True, True]]
    file: str = f'BTCUSDT-aggTrades-{dates_start[i].strftime("%Y-%m")}.csv'
    with open(f'/home/len/FutureTrading/tests/testData/batch/aggTrades/{file}', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        writer.writerows(data)

# Generate Ticks

"""
- Erzeugen von Tickdaten -> Müssen nicht soo sinnvoll sein, da Volumen in anderen Tests korrekt berechent wird 
- Für das Testen der Strategie, einzelne Daten und Testfälle
    - POC mitgeben
    - OHLC Daten
"""