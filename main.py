import sys
from typing import Final
import dataConfig as cfg
import datetime as dt

from util.lib.VolumeProfileGenerator import VolumeProfileGenerator


def main():
    # Process aggregated trades data
    src_file: str = 'BTCUSDT-aggTrades-2020-12.csv'
    dst_file: str = src_file
    chunk_size: Final[int] = 1000000
    vpg: VolumeProfileGenerator = VolumeProfileGenerator(cfg.AGTR_DP, cfg.AGTR_CNL, chunk_size, cfg.VOLP_DP)
    start: dt = dt.datetime(2020, 12, 24)
    end: dt = dt.datetime(2020, 12, 31, 23, 59, 59, 1000000 - 1)
    try:
        vpg.gen_volume_profile_interval(
            src_file=src_file,
            dst_file=dst_file,
            start_time=start.timestamp(),
            end_time=end.timestamp()
        )
    except ValueError as ve:
        print(ve)
    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sys.exit(main())

# See Pandas Intro for quick info https://github.com/efldatascience/ds-courses

