import numpy as np
import pandas as pd
from Util import Util

util = Util()

class DataLoading:
    def __init__(self, macro_data, market_data):
        self.macro_data = macro_data
        self.market_data = market_data

        self.pmi = None
        self.ppi = None
        self.cpi = None
        self.m0 = None
        self.m1 = None
        self.m2 = None
        self.rate_10yr = None
        self.rate_gap_10yr = None
        self.financing = None
        self.financing_delta = None
        self.a_index_erp = None
        self.sp500_erp = None
        self.sp500_vix = None

    def _arrange_data(self):

    def get_pmi(self):
        return self.pmi

    def get_pmi_12ma(self):
        return util.ma(self.pmi, 242)

