from CommonFunctions import conn2db
import pandas as pd
import numpy as np
from tqdm import tqdm

from Util import Util
from FactorGenerator import FactorGenerator

util = Util()
fg = FactorGenerator()

wind_conn = conn2db('wind_conn')
factors_conn = conn2db('factors_conn')
market_conn = conn2db('market_conn')

sector_code = pd.read_excel("中信证券一级行业指数.xlsx")
sector_valuation = dict(zip(sector_code.iloc[:, 0], [0 for _ in range(sector_code.shape[0])]))
sector_pv = dict(zip(sector_code.iloc[:, 0], [0 for _ in range(sector_code.shape[0])]))
sector_factors = dict(zip(sector_code.iloc[:, 0], [0 for _ in range(sector_code.shape[0])]))

a_share_index = (pd.read_sql(
    "select TRADE_DT, S_DQ_CLOSE from WANDE.wande.dbo.AINDEXWINDINDUSTRIESEOD where TRADE_DT>='%s' AND S_INFO_WINDCODE='%s'" %(
    '20121231', '881001.WI'), wind_conn)).sort_values(by=["TRADE_DT"], ignore_index=True)
a_share_index["DAILY_RETURN"] = a_share_index['S_DQ_CLOSE'].pct_change() * 100
a_share_index = (a_share_index.dropna(how='any')).reset_index(drop=True)

with tqdm(total=sector_code.shape[0], desc="FACTORS") as pbar:
#生成行业因子
    for code in sector_code.iloc[:, 0]:
        valuation = (pd.read_sql(
            "select TRADE_DT, PE_TTM, PB_LF, DIVIDEND_YIELD from WANDE.wande.dbo.AINDEXVALUATION where TRADE_DT >= '%s' AND S_INFO_WINDCODE = '%s';" % (
            20140101, code), wind_conn)).sort_values(by=['TRADE_DT'], ignore_index=True)
        pv = (pd.read_sql(
            "select TRADE_DT, S_DQ_CLOSE from WANDE.wande.dbo.AINDEXINDUSTRIESEODCITICS where TRADE_DT >= '%s' AND S_INFO_WINDCODE = '%s';" % (
            20121231, code), wind_conn)).sort_values(by=['TRADE_DT'], ignore_index=True)
        pv["DAILY_RETURN"] = pv["S_DQ_CLOSE"].pct_change() * 100
        pv = (pv.dropna(how='any')).reset_index(drop=True)
        beta = fg.beta(pv.loc[:, "DAILY_RETURN"], a_share_index.loc[:, "DAILY_RETURN"], pd.to_datetime(pv["TRADE_DT"]), 242)
        mom_242 = fg.mom(pv["S_DQ_CLOSE"], pd.to_datetime(pv["TRADE_DT"]), 242)
        vol_63 = fg.vol(pv["DAILY_RETURN"], pd.to_datetime(pv["TRADE_DT"]), 63)
        vol_63 = vol_63.loc[vol_63.index >= mom_242.index[0]]
        # 插入计算ZSCORE的utility function，之后做compound
        compounded_value = pd.DataFrame({"value": util.get_zcsore_static(np.divide(1, valuation.iloc[:, 1]) +
                                              util.get_zcsore_static(np.divide(1, valuation.iloc[:, 2])) +
                                              util.get_zcsore_static(valuation.iloc[:, 3]))})
        compounded_value.index = pd.to_datetime(valuation['TRADE_DT'])
        compounded_value.name = "value"
        factors = pd.DataFrame({})
        factors["mom_242"] = mom_242
        factors["beta"] = beta
        factors["vol_63"] = vol_63
        factors = factors.join(compounded_value)
        sector_pv[code] = pv
        sector_factors[code] = factors
        factors.to_excel("../行业轮动/factors/factors_%s.xlsx" % code)
