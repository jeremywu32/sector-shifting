import pandas as pd
import numpy as np

'''
use a dictionary to store the style factors of each sector
each item under the key is a dataframe with date index
backtesting frame goes like this:
- at the first step, calculate the standardised factor exposure of each style factor under its sector
- next, use utility functions to collect the statistics in the rolling window, visit each item in the dictionary
  via the list
- the output is expected to be a signal series
'''

class Util:
    def __init__(self):
        self._year = 242

    def ma(self, series: pd.DataFrame, period):
        return series.rolling(period).mean()

    def diff(self, series1, series2):
        return series1 - series2

    def median(self, series: pd.DataFrame, years):
        return series.rolling(years * self._year).median()

    def std(self, series: pd.DataFrame, years):
        return series.rolling(years * self._year).std()

    def series_diff(self, series: pd.DataFrame, period):
        diff = series - series.shift(period)
        diff = diff.dropna(how='any')
        return diff

    def get_zscore(self, series: pd.DataFrame, years):
        # series shall apply datetime index
        median = self.median(series, years)
        std = self.std(series, years)
        sub_series = series.loc[series.index >= median.index[0], ]
        return (sub_series - median) / std

