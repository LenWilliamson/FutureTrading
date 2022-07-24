import datetime
import sys
from typing import Final
import dataConfig as cfg
import datetime as dt

from util.lib.VolumeProfileGenerator import VolumeProfileGenerator


def main() -> int:
    # Process aggregated trades data
    src_file: str = 'BTCUSDT-aggTrades-2021-12.csv'
    dst_file: str = src_file
    chunk_size: Final[int] = 1000000
    vpg: VolumeProfileGenerator = VolumeProfileGenerator(cfg.AGTR_DP, cfg.AGTR_CNL, chunk_size, cfg.VOLP_DP)
    start: dt = dt.datetime(2021, 12, 25, 15, 0, 0, tzinfo=datetime.timezone.utc)
    end: dt = dt.datetime(2021, 12, 31)  # dt.datetime(2022, 1, 14, 23, 59, 59, 10 ** 6 - 1)
    print(f"{start.timestamp()}")
    # try:
    #     vpg.gen_volume_profile_interval(
    #         src_file=src_file,
    #         dst_file=dst_file,
    #         start_time=start.timestamp(),
    #         end_time=end.timestamp()
    #     )
    # except ValueError as ve:
    #     print(ve)
    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sys.exit(main())

# See Pandas Intro for quick info https://github.com/efldatascience/ds-courses

"""
TODOS:
 - Liste von .csv Dateien verabeiten und Volumen pro woche/tag/stunde berechnen (TESTEN)
 - (Multi Processing / Multi Threading / Functional: https://docs.python.org/3/howto/functional.html)
 - Logging reparieren und in Rust hinzufügen
 - CSV Monatsdateien ebenfalls splitten in woche/tag/stunde (als BatchProcessor)
 - Volumenproifl erstellen mit 1m klines über entsprechenden Zeitraum (dafür aber vorherigen Punkt erst erledigen)
"""