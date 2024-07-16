import pandas as pd
import numpy as np

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

