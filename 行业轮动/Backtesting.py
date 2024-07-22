import pandas as pd
import numpy as np
from datetime import timedelta
from collections import deque
from Classfier import Classfier

c = Classfier()

class Backtesting:
    def __init__(self, start_date, end_date, window_length, factor_nvs: pd.DataFrame, macro_indicators: dict):
        self._date_range = (pd.date_range(start=start_date, end=end_date, freq='D')).tolist()
        self._window_start = start_date
        self._window_end = None
        self._window_length = window_length
        self._factor_nvs = factor_nvs
        self._macro_indicators = macro_indicators
        self._style_episodes = {}

    '''
    traverse the date range list
    if datetime falls to the end of the month,
    visit the dictionaries to fetch the data of macro and factor reward
    do statistic on factor rewards to get factor performance
    put factor performance and macro performance into classfier to generate the final result
    '''

    def backtesting(self):
        for date in self._date_range:
            if ((date.month == 1 and date.day == 1) or (date.month == 2 and date.day == 1) or
                    (date.month == 3 and date.day == 1) or (date.month == 4 and date.day == 1) or
                    (date.month == 5 and date.day == 1) or (date.month == 6 and date.day == 1) or
                    (date.month == 7 and date.day == 1) or (date.month == 8 and date.day == 1) or
                    (date.month == 9 and date.day == 1) or (date.month == 10 and date.day == 1) or
                    (date.month == 11 and date.day == 1) or (date.month == 12 and date.day == 1)):
                self._window_end = date
                episode_score = [0, 0, 0, 0]
                for indicator in self._macro_indicators.keys():
                    if c.classify_macro(self._macro_indicators[indicator][date]) == 1:
                        factor_stats = self._compute_stats()
                        result = np.multiply(c.classify_styles(factor_stats), 1)
                        episode_score = np.add(episode_score, result)
                    elif c.classify_macro(self._macro_indicators[indicator][date]) == -1:
                        factor_stats = self._compute_stats(position_long=False)
                        result = np.multiply(c.classify_styles(factor_stats), -1)
                        episode_score = np.add(episode_score, result)
                self._style_episodes[date] = episode_score
                self._window_start = date + timedelta(days=1)

        return pd.DataFrame(self._style_episodes)


    def _compute_stats(self, position_long = True):
        stats = {}
        if position_long:
            factor_wrs = self._get_wr()
        else:
            factor_wrs = self._get_wr(position_long=False)

        #get median and prob from factor_wrs
        for key in factor_wrs.keys():
            result = [np.median((factor_wrs[key]))]
            pos = 0
            for wr in factor_wrs[key]:
                if wr > 0.5:
                    pos += 1
            result.append(pos / len(factor_wrs[key]))
            stats[key] = result
        return stats



    def _get_wr(self, position_long = True):
        '''
        use window start and window end to locate year frame
        resample the factor nv to month and get monthly return
        +ve return is valid at long position and -ve return is valid at short position
        calculate annual winning rate and append it into a list
        :param position_long:
        :return: A list of winning rates
        '''
        factor_wrs = {}
        monthly_nvs = self._factor_nvs.resample('M')
        monthly_nvs = monthly_nvs.loc[self._window_start : self._window_end + timedelta(days=1), :]
        window_size = 12
        # insert the calculation of wr
        # monthly nv should be wr
        for i in range(4):
            wr_series = []
            for j in range(window_size, monthly_nvs.shape[0] + 1, window_size):
                pos_count = 0
                for r in monthly_nvs.iloc[j - window_size:j, i]:
                    if position_long and r > 0:
                        pos_count += 1
                    elif not pos_count and r < 0:
                        pos_count += 1
                wr_series.append(pos_count / window_size)
            factor_wrs[i] = np.ndarray(wr_series)
        return factor_wrs



