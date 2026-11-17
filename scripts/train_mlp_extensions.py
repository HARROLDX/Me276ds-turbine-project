"""Exploratory fixed MLP ablations; never select settings using test scores."""
import json
import time
from pathlib import Path
import joblib
import pandas as pd
from threadpoolctl import threadpool_limits
from nox_project.data import load_development, load_test, TARGET
from nox_project.experiments import provenance, write_json
from nox_project.metrics import regression_metrics
from nox_project.models import build_model

root = Path.cwd()
out = root / 'runs/mlp-extensions-s276'
out.mkdir(parents=True, exist_ok=False)
choices = json.loads((root / 'configs/fixed_models.json').read_text())
base = choices['mlp']
# Keep the original column order, omitting only CDP. No new feature search.
reduced = [f for f in base['features'] if f != 'CDP']
variants = {
    'mlp': (base['features'], 0.01),
    'mlp_8': (reduced, 0.01),
    'mlp_no_l2': (base['features'], 0.0),
    'mlp_strong_l2': (base['features'], 0.1),
}
write_json(out / 'protocol.json', {
    'seed': 276, 'training': '2011-2014 plus first half of 2015',
    'test': 'second half of 2015; previously observed', 'validation_rows': 0,
    'interpretation': 'Exploratory follow-up after observing MLP test performance; no independent confirmation or selection of winner.',
    'feature_selection': 'Reuse historical eight-feature subset (omit CDP); no MLP feature search.',
    'variants': {k: {'features': f, 'params': {**base['params'], 'alpha': a}} for k, (f, a) in variants.items()},
})
write_json(out / 'provenance.json', provenance(root))
a, b = load_development(root)
train = pd.concat([a, b], ignore_index=True)
test = load_test(root)
pred = test[['row_id', 'year', TARGET]].copy()
rows = []
for key, (features, alpha) in variants.items():
    model = build_model('mlp', {**base['params'], 'alpha': alpha}, 276)
    start = time.perf_counter()
    with threadpool_limits(limits=1):
        model.fit(train[features], train[TARGET])
        pred[key] = model.predict(test[features])
    fitted = model.regressor_.named_steps['model']
    row = dict(model=key, n_features=len(features), alpha=alpha,
               n_iter=fitted.n_iter_, fit_seconds=time.perf_counter()-start,
               **regression_metrics(test[TARGET], pred[key]))
    rows.append(row)
    joblib.dump(model, out / f'{key}.joblib')
    pd.DataFrame(rows).to_csv(out / 'test_metrics.csv', index=False)
    pred.to_csv(out / 'test_predictions.csv', index=False)
    print(row, flush=True)
