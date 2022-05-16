from itertools import filterfalse
from typing import Dict, Callable, Any

import dataConfig as cfg
from typing import List, Final, Tuple
from unittest import TestCase

from util.lib.BatchProcessor import VolumeBatchProcessor
from util.lib.fileStorage import create_filename, find_files_recursive


class TestVolumeBatchProcessor(TestCase):
    """
    - AggTrades Daten für 3 Monate erstellen
    - Weekly, Days, Hours Volumen Profile test laufen lassen (genügend Daten produzieren=
    - Directory Struktur testen
    - Produzierten Ergebnisse testen
    """
    chunk_size: Final[int] = 7

    @classmethod
    def setUpClass(cls) -> None:
        print('setUpClass')
        cls.vbp: VolumeBatchProcessor = VolumeBatchProcessor(cfg.tAGTR_bDP, cfg.AGTR_CNL, cls.chunk_size, cfg.tVOLP_bDP)

    def test_process_batch(self) -> None:
        """
        Test to check if the test files are generated correctly:
         - we only check for file names, the VolumeProfileGenerator is tested differently
         - we check for every interval:
            - weeks
            - days
            - hours
        aufgrund der anderen Tests.
        :return: None/Void
        """

        # Test for weeks
        interval: Dict[str, int] = {'weeks': 1}
        offset: str = 'BTCUSDT-aggTrades-'
        self.vbp.process_batch(interval=interval, offset=offset, test=True)

        all_files: List[str] = find_files_recursive(root=cfg.tVOLP_bDP, ends_with='.csv')
        f: Callable[[Any], bool] = lambda x: True if 'test_' not in x else False
        target: List[str] = sorted(list(filter(f, all_files)))
        test: List[str] = sorted(list(filterfalse(f, all_files)), key=lambda x: x[5:])

        # Number of test files has to equal number of target files
        self.assertEqual(len(target), len(test))

        # Check for correct file names
        for trgt, tst in zip(target, test):
            with self.subTest(msg=test):
                self.assertEqual(trgt, tst[5:])
