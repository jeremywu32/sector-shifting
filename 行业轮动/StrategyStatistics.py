import numpy as np

import pandas as pd


class StrategyStatistics:

    def get_nv(self, series: pd.Series):
        nv = pd.DataFrame({"nv": [1 for _ in range(series.shape[0])]})
        nv.index = series.index
        for i in range(1, nv.shape[0]):
            nv.iloc[i] = nv.iloc[i - 1] * (1 + series.iloc[i] * 0.01)
        return nv

    def get_annualised_return(self, df, years):

        '''

        df: 资产净值

        years: 回测年数

        '''

        return float('%.2f' % (((df.iloc[-1, 1] / df.iloc[0, 1]) ** (1 / years) - 1) * 100))

    def get_alpha(self, strategy_yield, base_yield):

        '''

        strategy_yield: 策略收益

        base_yield: 基准收益

        '''

        return float('%.2f' % (strategy_yield - base_yield))

    def wrlr(self, date, nv, anv, trade_dt, resample_freq='na'):

        '''

        计算胜率赔率

        date: 从该日期后计算胜率赔率

        nv: 索引为datetime对象的净值序列

        anv: 索引为datetime类型的超额净值序列

        trade_dt: 调仓时间

        resample_freq: 计算月胜率或周胜率时进行时间重采样

        '''

        global freq_wr

        pos = []

        neg = []

        valid_freq = 0

        freq = 0

        if resample_freq == 'na':

            for i in range(1, len(trade_dt)):

                start = trade_dt[i - 1]

                end = trade_dt[i]

                if start >= date:

                    position_return = nv.loc[end, "NET_VALUE"] / nv.loc[

                        start, "NET_VALUE"] - 1

                    if position_return > 0:
                        valid_freq += 1

                    freq += 1

                    alpha_return = anv.loc[end, "NET_VALUE"] / anv.loc[

                        start, "NET_VALUE"] - 1

                    if alpha_return > 0:

                        pos.append(alpha_return)

                    else:

                        neg.append(alpha_return)

            freq_wr = float('%.2f' % (valid_freq / freq * 100))

        else:

            resampled_anv = anv.resample(resample_freq).last()

            resampled_anv = resampled_anv.loc[resampled_anv.index >= date,]

            resampled_anv = resampled_anv.dropna(how='any')

            for i in range(1, resampled_anv.shape[0]):

                alpha = resampled_anv.loc[resampled_anv.index[i], "NET_VALUE"] / resampled_anv.loc[

                    resampled_anv.index[i - 1], "NET_VALUE"] - 1

                if alpha > 0:

                    pos.append(alpha)

                else:

                    neg.append(alpha)

        winning_rate = float('%.2f' % (len(pos) / (len(pos) + len(neg)) * 100))

        losing_rate = float('%.2f' % (abs((sum(pos) / len(pos) / ((sum(neg) / len(neg)))))))

        print("freq_wr: ", freq_wr)

        print("wr: ", winning_rate)

        print("freq_lr ", losing_rate)

    def frame_slicer(self, df, date):

        '''

        df: 索引为datetime对象的数据

        date: 取该日期后的数据

        '''

        return df.loc[df.index >= date,]

    def maximum_withdrawn(self, df):

        '''

        df: 用于计算最大回撤的数据序列

        '''

        return float('%.2f' % (((1 - (df.iloc[:, 1] / df.iloc[:, 1].cummax()).min())) * 100))

    def ir(self, alpha, vol):

        '''

        alpha: 超额

        vol: 超额波动

        '''

        return float('%.3f' % (alpha / vol))

    def sharpe(self, strategy_yield, vol):

        '''

        strategy_yield: 策略收益

        vol: 策略波动

        '''

        return float('%.3f' % ((strategy_yield - 0.02) / vol))

    def peroidic_volatility(self, df):

        '''

        计算区间波动

        df: 日收益序列

        '''

        return float('%.2f' % ((np.std(df, ddof=1)) * 100))

    def annualised_volatility(self, df):

        '''

        计算年化波动

        df: 日收益序列

        '''

        return float('%.2f' % ((np.std(df, ddof=1) * np.sqrt(242)) * 100))