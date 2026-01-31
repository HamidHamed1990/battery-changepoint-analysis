import yaml
import os
import numpy as np
import pandas as pd

from src.io_utils import load_excel_sheets
from src.changepoint import extract_changepoints
from src.soh import collect_reference_capacity, compute_soh
from src.postprocess import reassign_cp_labels
from src.visualization import plot_example


with open("config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

df_capacity, df_voltage, df_dQdV, df_dVdQ = load_excel_sheets(cfg["input_excel"])

reference_capacity = collect_reference_capacity(df_capacity)

results = []
max_cp = {"voltage": 0, "dQdV": 0, "dVdQ": 0}

for i in range(len(df_capacity)):
    Q = df_capacity.iloc[i, 2:].dropna().reset_index(drop=True)
    V = df_voltage.iloc[i, 2:].dropna().reset_index(drop=True)
    dQdV = df_dQdV.iloc[i, 2:].dropna().reset_index(drop=True)
    dVdQ = df_dVdQ.iloc[i, 2:].dropna().reset_index(drop=True)

    min_len = min(len(Q), len(V), len(dQdV), len(dVdQ))
    Q, V, dQdV, dVdQ = Q[:min_len], V[:min_len], dQdV[:min_len], dVdQ[:min_len]

    cp_v = extract_changepoints(V, Q, **cfg["changepoint"])
    cp_qv = extract_changepoints(V, dQdV, **cfg["changepoint"])
    cp_vq = extract_changepoints(Q, dVdQ, **cfg["changepoint"])

    cell = int(df_capacity.iloc[i]["Cell"])
    soh = compute_soh(
        Q,
        cfg["soh"]["method"],
        reference_capacity.get(cell),
        cfg["soh"].get("nominal_capacity"),
    )

    max_cp["voltage"] = max(max_cp["voltage"], len(cp_v))
    max_cp["dQdV"] = max(max_cp["dQdV"], len(cp_qv))
    max_cp["dVdQ"] = max(max_cp["dVdQ"], len(cp_vq))

    results.append({
        "CellNumber": cell,
        "CycleNumber": int(df_capacity.iloc[i]["Cycle"]),
        "cp_voltage": cp_v,
        "cp_dQdV": cp_qv,
        "cp_dVdQ": cp_vq,
        "SOH": soh
    })

rows = []
for r in results:
    row = {k: r[k] for k in ["CellNumber", "CycleNumber", "SOH"]}
    for key in ["voltage", "dQdV", "dVdQ"]:
        for i in range(max_cp[key]):
            row[f"cp_{key}_{i+1}"] = (
                r[f"cp_{key}"][i] if i < len(r[f"cp_{key}"]) else np.nan
            )
    rows.append(row)

df_out = pd.DataFrame(rows)

if cfg["postprocessing"]["clustering"]:
    for key in ["voltage", "dQdV", "dVdQ"]:
        df_out = reassign_cp_labels(df_out, f"cp_{key}", max_cp[key])

df_out.to_csv(cfg["output_csv"], index=False)

if cfg["visualization"]["save_example"]:
    plot_example(df_capacity, df_voltage, df_dQdV, df_dVdQ, results, "example_plot.png")
