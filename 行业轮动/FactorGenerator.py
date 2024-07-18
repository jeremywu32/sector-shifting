import pandas as pd
import numpy as np
import statsmodels.api as sm


class FactorGenerator:
    def beta(self, sector_return_series: pd.Series, benchmark_series: pd.Series, time_label: pd.Series, window: int):
        betas = pd.Series(index=time_label.iloc[window:])
        betas.name = 'betas'
        for i in range(window, sector_return_series.shape[0]):
            regressor = ((benchmark_series.iloc[i - window : i + 1]).reset_index(drop=True)) - 0.02
            response = (sector_return_series.iloc[i - window : i + 1]).reset_index(drop=True)
            regressor = sm.add_constant(regressor)
            model = sm.OLS(response, regressor).fit()
            betas.iloc[i - window] = model.params.iloc[1]
        return betas

    def mom(self, price_series: pd.Series, time_label: pd.Series, days):
        tl = time_label[days:]
        prior_price_series = price_series.shift(days)
        prior_price_series = prior_price_series
        mom = (price_series.div(prior_price_series)).dropna(how='any')
        mom.index = tl
        mom.name = 'mom'
        return mom

    def vol(self, return_series: pd.Series, time_label: pd.Series, days):
        tl = time_label[days - 1:]
        vol = return_series.rolling(days).std()
        vol = vol.dropna(how='any')
        vol.index = tl
        vol.name = 'vol'
        return vol


