import concurrent.futures
import datetime as dt
import os
import sys
from abc import abstractmethod
from functools import partial
from typing import Final, List, Dict, Tuple, Callable
from dateutil.relativedelta import relativedelta

import dataConfig as cfg
from util.lib.VolumeProfileGenerator import VolumeProfileGenerator
from util.lib.fileStorage import create_filename
from util.lib.timeConverter import time_converter, date_time_generator


class BatchProcessor:
    def __init__(self, batch_dir: str):
        """

        :param batch_dir:
        """
        self.bd_bytes: Final[bytes] = os.fsencode(batch_dir)
        self.bd_str: Final[str] = batch_dir

    @abstractmethod
    def process_batch(self, interval: int, offset: str, test: bool = False) -> None:
        raise NotImplementedError('Subclasses should implement this!')


def _out_files(file: str, ts: List[Tuple[dt.datetime, dt.datetime]]) -> List[str]:
    """
    TODO
    :param file:
    :param ts:
    :return:
    """
    f: Callable[[Tuple[dt.datetime, dt.datetime]], str] = partial(create_filename, file=file)
    return list(map(f, ts))


class VolumeBatchProcessor(BatchProcessor):
    def __init__(self, batch_dir: str, column_names: List[str], chunk_size: int, destination_path: str):
        """

        :param batch_dir:
        :param column_names:
        :param chunk_size:
        :param destination_path:
        """
        BatchProcessor.__init__(self, batch_dir=batch_dir)
        self.vpg: Final[VolumeProfileGenerator] = VolumeProfileGenerator(
            data_source=batch_dir,
            column_names=column_names,
            chunk_size=chunk_size,
            destination_path=destination_path
        )

    def process_batch(self, interval: Dict[str, int], offset: str, test: bool = False) -> None:
        """
        TODO -> Es werden aktuell nur die Typen für interval akzeptiert wie sie im "Example" stehen
            start = time.perf_counter()
            finish = time.perf_counter()
            print(f'Finished in {round(finish-start, 2)} second(s)')
            Erkläre -1/10**6, da ich ja immer abgeschlossenes bis offenes Intervall haben möchte
        :param offset: If we process an aggTrades batch the offset is 'BTCUSDT-aggTrades-'
        :param interval: Time interval in hours that should be filtered
            Example:
                ['hours',3] = three hours
                ['days',2] = two days
                ['weeks',1] = one week
        :param test:
        :return: None/Void
        """
        cfg.LOGGER.debug(
            f'{sys.argv[0]} :: CALL :: VolumeBatchProcessor(BatchProcessor).process_batch({interval}, {offset}, {test})')

        filenames = map(
            os.fsdecode,
            filter(
                lambda x: os.fsdecode(filename=x).endswith('.csv'),
                os.listdir(self.bd_bytes)
            )
        )
        for file in filenames:
            open_dt: dt.datetime = dt.datetime.strptime(file[len(offset):-4], '%Y-%m')
            # Assumption: Aggregated trades data has a relative delta of exactly one month
            end_dt: dt.datetime = open_dt + relativedelta(months=1)
            # Generate list of datetime stamps
            lof_dt: List[dt.datetime] = list(
                date_time_generator(start=open_dt, end=end_dt, delta=dt.timedelta(**interval))
            )

            # Zip list of datetime stamps into tuples of (start, end) datetime objects
            lof_start_end: List[Tuple[dt.datetime, dt.datetime]] = list(zip(lof_dt[:-1], lof_dt[1:]))
            # Number of output files
            n: int = len(lof_start_end)

            args_src_file = [file for _ in range(n)]
            args_dst_file = [out if not test else 'test_' + out for out in args_src_file]
            args_start_time: List[dt.datetime] = [s for s, _ in lof_start_end]
            args_end_time: List[dt.datetime] = [e for _, e in lof_start_end]
            args_sub_dirs: List[List[str]] = [[time_converter(time_stamp=open_dt.timestamp()), list(interval.keys())[0]] for _ in range(n)]
            args = [
                args_src_file,
                args_dst_file,
                [x.timestamp() for x in args_start_time],
                [x.timestamp() for x in args_end_time],
                args_sub_dirs
            ]

            # for i in range(n):
            #     self.vpg.gen_volume_profile_interval(
            #         src_file=args_src_file[i],
            #         dst_file=args_dst_file[i],
            #         start_time=args_start_time[i].timestamp(),
            #         end_time=args_end_time[i].timestamp(),
            #         sub_dirs=args_sub_dirs[i]
            #     )

            with concurrent.futures.ProcessPoolExecutor() as executor:
                executor.map(self.vpg.gen_volume_profile_interval, *args)
        """
        1. Prüfen der Speichern Methode -> Ggf. auslagern? (TESTEN -> DONE)
        2. Output Directory definieren /weekly_ts/files.csv ... (TESTEN -> DONE, da die save_data Funktion getestet ist)
        -> Du musst noch date_time_generator testen
        +++ => Teste process_batch
        Wenn alle Tests geschrieben sind:
        1. Test Directory anpassen in util/lib und util/functionalLib
        2*. For Loop in eine Map Funktion umschreiben mit mehreren kleinen Funktionen
        2**. Doku schreiben -> https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
        3. Kann ich noch wo anders multiproccessing machen?
        4. Logging und Multiprocessing (Erstmal das Loggen auskommentieren)
        """

    def _add_path(self, filename: str) -> str:
        return self.bd_str + filename


# vbp = VolumeBatchProcessor('/home/len/FutureTrading/data/test', [''], 0, '')
# vbp.process_batch(0, offset='fake_')
# import time
# def thread_function(name, number):
#     print(f"Thread {name},{number}: starting")
#     time.sleep(number)
#     return f"Thread {name},{number}: finishing"
#
#
# if __name__ == "__main__":
#     start = time.perf_counter()
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         args = [i for i in range(10)]
#         b = [args, args]
#         results: Iterator[str] = executor.map(thread_function, *b)
#         for r in results:
#             print(r)
#     finish = time.perf_counter()
#     print(f'Finished in {round(finish-start, 2)} second(s)')

# d = {'minutes': 246}
# g = list(date_time_generator(dt.datetime(2011, 10, 10), dt.datetime(2011, 10, 11), dt.timedelta(**d)))
# for result in date_time_generator(dt.datetime(2011, 10, 10), dt.datetime(2011, 10, 11), dt.timedelta(**d)):
#     print(result)
#
# for i, j in zip(g[:-1], g[1:]):
#     print(f'start={i} end={j}')