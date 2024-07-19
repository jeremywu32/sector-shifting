import pandas as pd
import numpy as np
import statsmodels.api as sm
import numba


class CSR:
    def __init__(self, factors: dict, sector_return: dict, time_label: pd.Series, ):
        self._factors = factors
        self._time_label = time_label
        self._sector_return = sector_return

    def cross_session_regression(self, factor_name: str):
        factor_return = pd.Series(index=self._time_label, name=factor_name)
        regressor_set = self._create_regressor(factor_name)
        regressor_set.fillna(0, inplace=True)
        response_set = self._create_response()
        response_set.fillna(0, inplace=True)
        for i in range(regressor_set.shape[0]):
            response = np.asarray(response_set.iloc[i]).T
            regressor = np.asarray(regressor_set.iloc[i])
            regressor = sm.add_constant(regressor)
            model = sm.OLS(response, regressor).fit()
            factor_return.iloc[i] = model.params[1]
        return factor_return

    def _create_regressor(self, factor_name: str):
        regressor = pd.DataFrame(index=self._time_label)
        for sector in self._factors.keys():
            regressor[sector] = self._factors[sector][factor_name]
        return regressor

    def _create_response(self):
        response = pd.DataFrame(index=self._time_label)
        for sector in self._sector_return.keys():
            response[sector] = self._sector_return[sector]["DAILY_RETURN"]
        return response
