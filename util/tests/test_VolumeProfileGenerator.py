import filecmp
import os
from typing import List, Final
from unittest import TestCase

from util.lib.VolumeProfileGenerator import VolumeProfileGenerator


class TestVolumeProfileGenerator(TestCase):
    # @classmethod
    # def setUpClass(cls) -> None:
    #     print('setUpClass')

    def setUp(self) -> None:
        # print('setUp')
        self.pwd: str = os.getcwd()
        agg_trades_data_path: str = os.path.join(self.pwd, 'testData', 'aggTrades', 'td1.csv')
        agg_trades_column_names: List[str] = ['AggTradeId', 'Price', 'Quantity', 'FirstTradeId',
                                              'LastTradeId', 'Timestamp', 'Buyer=Maker', 'BestTradPriceMatch']
        chunk_size: Final[int] = 7
        self.vpg: VolumeProfileGenerator = VolumeProfileGenerator(agg_trades_data_path, agg_trades_column_names,
                                                                  chunk_size,
                                                                  os.path.join(self.pwd, 'testData',
                                                                               'volumeProfile'), 'test.csv')

    # def tearDown(self) -> None:
    #     print('tearDown')

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     print('tearDownClass')

    def test_generate_volume_profile(self):
        self.vpg.generate_volume_profile()
        target: str = os.path.join(self.pwd, 'testData', 'volumeProfile', 'td1.csv')
        test: str = os.path.join(self.pwd, 'testData', 'volumeProfile', 'test.csv')
        self.assertEqual(True, filecmp.cmp(test, target, shallow=True))
