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

    '''
    general assumption: data is at monthly frequency
                        dataframes are datetime indexed
    那个啥，你的返回类型可能会爆炸~~~~~~~~
    '''

    def get_zcsore_static(self, series: pd.DataFrame):
        mean = np.mean(series)
        std = np.std(series)
        diff = series - [mean for _ in range(series.shape[0])]
        return np.divide(diff, std)

    def get_zscore_rolling(self, series: pd.DataFrame, years):
        # series shall apply datetime index
        median = self.median(series, years)
        std = self.std(series, years)
        sub_series = series.loc[series.index >= median.index[0], ]
        return (sub_series - median) / std

    def get_sue_3yr(self, series: pd.DataFrame):
        past_3yr_series = series.shift(36)
        past_3yr_series = past_3yr_series.dropna(how='any')
        benchmark_time = past_3yr_series.index[0]
        past_2yr_series = series.shift(24)
        past_2yr_series = past_2yr_series.dropna(how='any')
        past_2yr_series = past_2yr_series.loc[past_2yr_series.index >= benchmark_time, ]
        past_1yr_series = series.shift(12)
        past_1yr_series = past_1yr_series.dropna(how='any')
        past_1yr_series = past_1yr_series.loc[past_1yr_series.index >= benchmark_time, ]
        current_series = series.loc[series.index >= benchmark_time, ]
        std = self.std(series, 3)
        past_ave_series = np.divide(past_1yr_series.iloc[:, 0] + past_2yr_series.iloc[:, 0] + past_3yr_series.iloc[:, 0], 3)
        past_ave_series.index = past_3yr_series.index
        return (current_series - past_ave_series) / std

    def marginal_change(self, series: pd.DataFrame):
        three_mo_ago = series.shift(3)
        three_mo_ago = three_mo_ago.dropna(how='any')
        return series - three_mo_ago
