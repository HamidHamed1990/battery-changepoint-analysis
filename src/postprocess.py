# Post-processing utilities
import numpy as np
from sklearn.cluster import KMeans

def reassign_cp_labels(df, prefix, max_cp):
    if max_cp < 1:
        return df

    values, mapping = [], []

    for idx, row in df.iterrows():
        for i in range(max_cp):
            val = row.get(f"{prefix}_{i+1}", np.nan)
            if not np.isnan(val):
                values.append([val])
                mapping.append(idx)

    if len(values) < max_cp:
        return df

    kmeans = KMeans(n_clusters=max_cp, random_state=42, n_init="auto")
    labels = kmeans.fit_predict(values)
    centers = kmeans.cluster_centers_.flatten()

    order = np.argsort(centers)
    remap = {old: new for new, old in enumerate(order)}

    new_cols = {i: {} for i in range(max_cp)}
    for i, idx in enumerate(mapping):
        new_cols[remap[labels[i]]][idx] = values[i][0]

    for i in range(max_cp):
        df[f"{prefix}_{i+1}"] = [
            new_cols[i].get(idx, np.nan) for idx in range(len(df))
        ]

    return df
