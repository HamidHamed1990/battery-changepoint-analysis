# Change point detection
import ruptures as rpt

def extract_changepoints(x, y, model="rbf", penalty=10, jump=1):
    if len(y.dropna()) < 4:
        return []

    algo = rpt.Pelt(model=model, jump=jump).fit(y.values)
    result = algo.predict(pen=penalty)

    indices = [i - 1 for i in result if 0 < i < len(x)]
    return list(x.iloc[indices].values)

