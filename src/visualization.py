# Plotting and visualization
import matplotlib.pyplot as plt
import random

def plot_example(df_capacity, df_voltage, df_dQdV, df_dVdQ, results, filename):
    example = random.choice(results)

    cell = example["CellNumber"]
    cycle = example["CycleNumber"]

    idx = df_capacity[
        (df_capacity["Cell"] == cell) &
        (df_capacity["Cycle"] == cycle)
    ].index[0]

    Q = df_capacity.iloc[idx, 2:].dropna().reset_index(drop=True)
    V = df_voltage.iloc[idx, 2:].dropna().reset_index(drop=True)
    dQdV = df_dQdV.iloc[idx, 2:].dropna().reset_index(drop=True)
    dVdQ = df_dVdQ.iloc[idx, 2:].dropna().reset_index(drop=True)

    min_len = min(len(Q), len(V), len(dQdV), len(dVdQ))
    Q, V, dQdV, dVdQ = Q[:min_len], V[:min_len], dQdV[:min_len], dVdQ[:min_len]

    plt.figure(figsize=(15, 4))

    plt.subplot(1, 3, 1)
    plt.plot(Q, V)
    for cp in example["cp_voltage"]:
        plt.axhline(cp, ls="--", c="r")
    plt.xlabel("Capacity (Q)")
    plt.ylabel("Voltage (V)")

    plt.subplot(1, 3, 2)
    plt.plot(V, dQdV)
    for cp in example["cp_dQdV"]:
        plt.axvline(cp, ls="--", c="g")
    plt.xlabel("Voltage (V)")
    plt.ylabel("dQ/dV")

    plt.subplot(1, 3, 3)
    plt.plot(Q, dVdQ)
    for cp in example["cp_dVdQ"]:
        plt.axvline(cp, ls="--", c="b")
    plt.xlabel("Capacity (Q)")
    plt.ylabel("dV/dQ")

    plt.tight_layout()
    plt.savefig(filename, dpi=600)
    plt.show()
