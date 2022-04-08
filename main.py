import sys
from typing import Final
import dataConfig as cfg

from util.lib.VolumeProfileGenerator import VolumeProfileGenerator


def main():
    # Process aggregated trades data
    src_file: str = 'BTCUSDT-aggTrades-2021-01.csv'
    dst_file: str = src_file
    chunk_size: Final[int] = 1000000
    vpg: VolumeProfileGenerator = VolumeProfileGenerator(cfg.AGTR_DP, cfg.AGTR_CNL, chunk_size, cfg.VOLP_DP)
    vpg.gen_volume_profile(src_file_name=src_file, dst_file_name=dst_file)
    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sys.exit(main())

# See Pandas Intro for quick info https://github.com/efldatascience/ds-courses
