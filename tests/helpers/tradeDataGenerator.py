import csv
import datetime as dt
from functools import partial
from typing import List, Any, Callable

from util.functionalLib.functional import foldl
from util.lib.timeConverter import date_time_generator, time_converter

header = [
    'AggTradeId', 'Price', 'Quantity', 'FirstTradeId', 'LastTradeId',
    'Timestamp', 'Buyer=Maker', 'BestTradPriceMatch'
]
no_test_cases: int = 4
dates_start = [dt.datetime(2000, m + 1, 1) for m in range(no_test_cases)]
dates_end = [dt.datetime(2000, m + 2, 1) for m in range(no_test_cases)]
timedelta = [dt.timedelta(hours=1) for _ in range(no_test_cases)]
price = [i + 1 for i in range(no_test_cases)]

print(dates_start)
print(dates_end)
print(timedelta)


def append_row(rows: List[Any], x: dt.datetime, px: int) -> List[Any]:
    """
    [a] -> a -> [a] ++ [a], wehre a is of specific format
    :param rows: Accumulator
    :param x: Element that we add to tail of rows
    :param px: Traded price (dummy)
    :return: [a] -> a -> [a] ++ [a]
    """
    return rows + [[482561652, 1000 * px, 1, 536781294, 536781297, time_converter(x.timestamp(), blank=True), True, True]]


def write_aggTrades_data(start: dt.datetime, end: dt.datetime, delta: dt.timedelta, px: int) -> None:
    """
    Writes a dummy aggTrades file and stores it in hard coded path
    :param start: Start timestamp of generated data
    :param end: End timestamp of generated data
    :param delta: Timedelta between start and end
    :param px: Traded price (dummy)
    :return: None/Void
    """
    f: Callable[[List[Any], dt.datetime], List[Any]] = partial(append_row, px=px)
    data: List[List[Any]] = foldl(
        f=f,
        acc=[],
        xs=date_time_generator(start=start, end=end, delta=delta)
    )
    file: str = f'BTCUSDT-aggTrades-{start.strftime("%Y-%m")}.csv'
    with open(f'/home/len/FutureTrading/tests/testData/batch/aggTrades/{file}', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        # writer.writerow(header)

        # write the data
        writer.writerows(data)


def gen_aggTrades_date() -> None:
    """
    Map evaluation is lazy. We have to consume elements for map being executed.
    Instead use Pythonic list comprehension.
    :return: None/Void
    """
    for _ in map(write_aggTrades_data, dates_start, dates_end, timedelta, price):
        pass


