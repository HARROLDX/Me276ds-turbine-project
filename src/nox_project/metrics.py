import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error


def regression_metrics(y, prediction):
    if not np.isfinite(prediction).all():
        raise ValueError("Non-finite predictions")
    return {
        "mae": float(mean_absolute_error(y, prediction)),
        "rmse": float(root_mean_squared_error(y, prediction)),
        "r2": float(r2_score(y, prediction)),
    }
