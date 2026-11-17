"""Refit fixed historical choices with additional labeled data; no new tuning."""
import json
from pathlib import Path
import joblib
import pandas as pd
from nox_project.data import load_development, load_test, TARGET
from nox_project.experiments import fit_record, provenance, write_json
from nox_project.models import build_model
from threadpoolctl import threadpool_limits

root=Path.cwd()
out=root/"runs/expanded-s276"
out.mkdir(parents=True,exist_ok=False)
old=json.loads((root/"results/final-s276/selection.json").read_text())
a,b=load_development(root)
train=pd.concat([a,b],ignore_index=True)
test=load_test(root)
write_json(out/"provenance.json",provenance(root))
pred=test[["row_id","year",TARGET]].copy()
rows=[]
for key,choice in old["selected"].items():
    import time
    from nox_project.metrics import regression_metrics
    m=build_model(choice["model"],choice["params"],old["seed"])
    start=time.perf_counter()
    with threadpool_limits(limits=1):
        m.fit(train[choice["features"]],train[TARGET])
        y=m.predict(test[choice["features"]])
    pred[key]=y
    rows.append(dict(model=key,n_features=len(choice["features"]),fit_seconds=time.perf_counter()-start,**regression_metrics(test[TARGET],y)))
    joblib.dump(m,out/f"{key}.joblib")
    print(rows[-1],flush=True)
pred.to_csv(out/"test_predictions.csv",index=False)
pd.DataFrame(rows).to_csv(out/"test_metrics.csv",index=False)
write_json(out/"protocol.json",{"training_rows":len(train),"test_rows":len(test),"validation_rows":0,"parameters":"fixed from final-s276 historical selection; previously used 2015 first half for selection","test":"same previously observed 2015 second half; comparison is exploratory","selected":old["selected"]})
