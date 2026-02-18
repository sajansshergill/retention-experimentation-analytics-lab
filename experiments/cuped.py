from __future__ import annotations
import numpy as np
import pandas as pd

def cuped_adjust(
    df: pd.DataFrame,
    outcome_col: str,
    preperiod_col: str,
    group_col: str = "variant",
) -> pd.Series:
    """
    CUPED: Y_adj = Y - theta*(X - mean(X))
    where theta = cov(Y, X) / var(X)
    """
    d = df[[outcome_col, preperiod_col, group_col]].dropna()
    y = d[outcome_col].astype(float).to_numpy()
    x = d[preperiod_col].astype(float).to_numpy()
    
    vx = np.var(x, ddof = 1)
    if vx == 0:
        return df[outcome_col].astype(float) # no adjustment possible
    
    theta = np.cov(y, x, ddof=1)[0, 1] / vx
    x_mean = np.mean(x)
    
    adj = df[outcome_col].astype(float) - theta * (df[preperiod_col].astype(float) - x_mean)
    return adj