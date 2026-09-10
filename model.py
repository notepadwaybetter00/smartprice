def linear_fit(ys):
    """Least-squares fit of y = m*x + c. Returns (slope, intercept, r_squared)."""
    n = len(ys)
    if n < 2:
        return 0.0, (ys[0] if ys else 0.0), 0.0
    xs = list(range(n))
    x_mean = sum(xs) / n
    y_mean = sum(ys) / n
    num = den = 0.0
    for x, y in zip(xs, ys):
        num += (x - x_mean) * (y - y_mean)
        den += (x - x_mean) ** 2
    slope = num / den if den else 0.0
    intercept = y_mean - slope * x_mean

    ss_res = ss_tot = 0.0
    for i, y in enumerate(ys):
        pred = slope * i + intercept
        ss_res += (y - pred) ** 2
        ss_tot += (y - y_mean) ** 2
    r2 = 1 - ss_res / ss_tot if ss_tot else 0.0
    return slope, intercept, r2


def predict_prices(history, steps=2):
    """Predict the price 'steps' weeks ahead using linear regression.

    Returns a list of predicted prices for the next `steps` weeks.
    """
    ys = [float(p) for p in history]
    slope, intercept, _ = linear_fit(ys)
    last_x = len(ys) - 1
    predictions = [slope * (last_x + k + 1) + intercept for k in range(steps)]
    return [round(max(1, p)) for p in predictions]