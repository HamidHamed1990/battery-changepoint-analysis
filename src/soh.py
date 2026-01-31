# State of Health calculations
import numpy as np

def collect_reference_capacity(df_capacity):
    ref = {}
    for _, row in df_capacity.iterrows():
        if int(row["Cycle"]) == 2:
            Q = row.iloc[2:].dropna()
            if len(Q) > 0:
                ref[int(row["Cell"])] = Q.iloc[-1]
    return ref


def compute_soh(Q, method, reference=None, nominal_capacity=None):
    if len(Q) == 0:
        return np.nan

    if method == "cycle2":
        return Q.iloc[-1] / reference if reference else np.nan

    if method == "nominal":
        return Q.iloc[-1] / nominal_capacity

    raise ValueError("Unknown SOH method")
