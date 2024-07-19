import numpy as np
import pandas as pd
from Util import Util

util = Util()

'''
use a dictionary to store the style factors of each sector
each item under the key is a dataframe with date index
backtesting frame goes like this:
- at the first step, calculate the standardised factor exposure of each style factor under its sector
- next, use utility functions to collect the statistics in the rolling window, visit each item in the dictionary
  via the list
- the output is expected to be a signal series
'''

class DataLoading:
    def __init__(self, macro_data: pd.DataFrame, bond_data: pd.DataFrame, market_data: pd.DataFrame, init_date):
        self._macro_data = macro_data.loc[market_data.index >= init_date, ]
        self._bond_data = bond_data.loc[bond_data.index >= init_date, ]
        self._market_data = market_data.loc[market_data.index >= init_date, ]
        self._macro_dict = {}

        self._pmi = None
        self._ppi = None
        self._cpi = None
        self._m0 = None
        self._m1 = None
        self._m2 = None
        self._rate_10yr = None
        self._rate_gap_10yr = None
        self._financing = None
        self._financing_delta = None
        self._a_index_erp = None
        self._sp500_erp = None
        self._sp500_vix = None

    def _arrange_data(self):
        # group data into class A and class B
        # handle time lagging problem
        self._macro_dict['pmi'] = self._macro_data.iloc[:, 2]
        self._macro_dict['pmi'].index = self._market_data.index
        self._macro_dict['pmi_ma12'] = util.ma(self._macro_data.iloc[:, 2], 242)
        self._macro_dict['pmi_ma12'].index = self._market_data.index
        self._macro_dict['ppi'] = (self._macro_data.iloc[:, 3]).shift(1)
        self._macro_dict['ppi'].index = self._macro_data.index
        self._macro_dict['cpi'] = (self._macro_data.iloc[:, 1]).shift(1)
        self._macro_dict['cpi'].index = self._macro_data.index
        self._macro_dict['m0'] = (self._macro_data.iloc[:, 5]).shift(1)
        self._macro_dict['m0'].index = self._macro_data.index
        self._macro_dict['m1'] = (self._macro_data.iloc[:, 6]).shift(1)
        self._macro_dict['m1'].index = self._macro_data.index
        self._macro_dict['m2'] = (self._macro_data.iloc[:, 7]).shift(1)
        self._macro_dict['m2'].index = self._macro_data.index
        self._macro_dict['m1_m0'] = (self._macro_data.iloc[:, 6] - self._macro_data.iloc[:, 5]).shift(1)
        self._macro_dict['m1_m0'].index = self._macro_data.index
        self._macro_dict['rate_10yr'] = self._bond_data.iloc[:, 2]
        self._macro_dict['rate_10yr'].index = self._macro_data.index
        self._macro_dict['rate_gap_10yr'] = self._bond_data.iloc[:, 2] - self._bond_data.iloc[:, 1]
        self._macro_dict['rate_gap_10yr'].index = self._macro_data.index
        self._macro_dict['financing'] = (self._macro_data.iloc[:, 7]).shift(1)
        self._macro_dict['financing'].index = self._macro_data.index
        self._macro_dict['financing_delta'] = (self._macro_data.iloc[:, 8]).shift(1)
        self._macro_dict['financing_delta'].index = self._macro_data.index
        self._macro_dict['a_share_index_erp'] = self._set_a_share_index_erp()
        self._macro_dict['a_share_index_erp'].index = self._macro_data.index
        self._macro_dict['sp500_erp'] = self._set_sp500_erp()
        self._macro_dict['sp500_erp'].index = self._macro_data.index
        self._macro_dict['sp500_vix'] = self._set_sp500_vix()
        self._macro_dict['sp500_vix'].index = self._macro_data.index

    def get_macro_dict(self):
        return self._macro_dict

    def _set_a_share_index_erp(self):
        return self._a_index_erp

    def _set_sp500_erp(self):
        return self._sp500_erp

    def _set_sp500_vix(self):
        return self._sp500_vix



