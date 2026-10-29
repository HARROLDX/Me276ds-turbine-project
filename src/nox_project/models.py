"""Course models with preprocessing enclosed in each estimator."""

from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_model(name, params, seed):
    options = dict(params)
    if name == "ols":
        estimator = LinearRegression(**options)
    elif name == "ridge":
        estimator = Ridge(**options)
    elif name == "lasso":
        estimator = Lasso(max_iter=20000, **options)
    elif name == "random_forest":
        return RandomForestRegressor(random_state=seed, n_jobs=1, **options)
    elif name == "gradient_boosting":
        return GradientBoostingRegressor(random_state=seed, **options)
    elif name == "mlp":
        if "hidden_layer_sizes" in options:
            options["hidden_layer_sizes"] = tuple(options["hidden_layer_sizes"])
        estimator = MLPRegressor(random_state=seed, early_stopping=False, max_iter=500, **options)
    else:
        raise ValueError(f"Unknown model: {name}")
    pipeline = Pipeline([("scale", StandardScaler()), ("model", estimator)])
    # Target scaling helps MLP optimization; inverse_transform returns mg/m^3.
    if name == "mlp":
        return TransformedTargetRegressor(regressor=pipeline, transformer=StandardScaler())
    return pipeline
