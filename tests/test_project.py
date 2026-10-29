"""No model fitting in this suite, including fixtures and synthetic report checks."""

import json
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
from sklearn.base import clone
from sklearn.exceptions import NotFittedError
from sklearn.model_selection import ParameterGrid
from sklearn.utils.validation import check_is_fitted

from nox_project.cli import main
from nox_project.data import (
    COLUMNS,
    FEATURES,
    TARGET,
    audit,
    download,
    load_development,
    load_test,
    partition_holdout,
    sha256,
    validate_frame,
)
from nox_project.experiments import check_frozen, choose_features, dry_run, evaluate, load_config
from nox_project.metrics import regression_metrics
from nox_project.models import build_model

ROOT = Path(__file__).resolve().parents[1]


def test_raw_integrity_and_split():
    result = audit(ROOT)
    assert result["total_rows"] == 36733
    train, validation = load_development(ROOT)
    test = load_test(ROOT)
    assert (len(train), len(validation), len(test)) == (29349, 3692, 3692)
    assert set(train.year) == {2011, 2012, 2013, 2014}
    assert set(validation.year) == set(test.year) == {2015}
    assert validation.row_id.iloc[-1] == "2015:3691"
    assert test.row_id.iloc[0] == "2015:3692"
    assert set(train.row_id).isdisjoint(validation.row_id)
    assert set(train.row_id).isdisjoint(test.row_id)
    assert set(validation.row_id).isdisjoint(test.row_id)
    assert len(FEATURES) == 9
    assert not {"CO", TARGET, "year", "row_id"}.intersection(FEATURES)


def test_holdout_partition_does_not_share_rows_or_mutable_values():
    frame = pd.DataFrame({"NOX": range(9)})
    validation, test = partition_holdout(frame)
    assert validation.NOX.tolist() == [0, 1, 2, 3]
    assert test.NOX.tolist() == [4, 5, 6, 7, 8]
    test.loc[:, "NOX"] = -1
    assert validation.NOX.tolist() == [0, 1, 2, 3]
    assert frame.NOX.tolist() == list(range(9))


@pytest.mark.parametrize("bad", [np.nan, np.inf, -np.inf])
def test_nonfinite_rejected(bad):
    frame = pd.DataFrame(np.ones((4, 11)), columns=COLUMNS)
    frame.loc[0, "AT"] = bad
    with pytest.raises(ValueError, match="non-finite"):
        validate_frame(frame)


def test_wrong_columns_rejected():
    with pytest.raises(ValueError, match="columns"):
        validate_frame(pd.DataFrame({"NOX": [1]}))


def test_all_candidates_clone_and_remain_unfitted():
    config = load_config(ROOT / "configs/experiments.json")
    for name, grid in config["models"].items():
        for params in ParameterGrid(grid):
            model = clone(build_model(name, params, config["seed"]))
            with pytest.raises(NotFittedError):
                check_is_fitted(model)
            if name == "mlp":
                assert not model.regressor.named_steps["model"].early_stopping
            if name == "random_forest":
                assert model.n_jobs == 1


def test_dry_run_does_not_fit():
    config = load_config(ROOT / "configs/experiments.json")
    with patch("sklearn.pipeline.Pipeline.fit", side_effect=AssertionError("No fitting allowed")):
        result = dry_run(ROOT, config)
    assert result["training_performed"] is False
    assert result["total_development_fits"] == 73
    assert result["rows"] == {"train": 29349, "validation": 3692, "test": 3692}


@pytest.mark.parametrize("command", ["develop", "evaluate"])
def test_training_requires_explicit_execute(command, tmp_path):
    run = tmp_path / "never-created"
    with pytest.raises(SystemExit) as exc:
        main([command, "--run", str(run)])
    assert exc.value.code == 2
    assert not run.exists()


def test_metrics_in_original_units():
    scores = regression_metrics([1, 2, 3], np.array([1, 2, 4]))
    assert scores["mae"] == pytest.approx(1 / 3)
    assert scores["rmse"] == pytest.approx(np.sqrt(1 / 3))
    assert scores["r2"] == pytest.approx(0.5)


def test_feature_choice_prefers_smallest_within_tolerance():
    path = [
        {"n_features": k, "validation": {"rmse": e}}
        for k, e in [(1, 11), (2, 10.09), (3, 10), (4, 10.05)]
    ]
    assert choose_features(path, 0.01)["n_features"] == 2
    assert choose_features(path, 0)["n_features"] == 3


def test_download_is_offline_when_complete_and_refuses_modified_data(tmp_path):
    with patch("nox_project.data.urlopen", side_effect=AssertionError("No network needed")):
        assert download(ROOT)["downloaded"] == []
    (tmp_path / "data/raw").mkdir(parents=True)
    (tmp_path / "data/manifest.json").write_bytes((ROOT / "data/manifest.json").read_bytes())
    (tmp_path / "data/raw/gt_2011.csv").write_text("modified")
    with pytest.raises(ValueError, match="refusing to overwrite"):
        download(tmp_path)


def test_frozen_selection_detects_edits(tmp_path):
    selection = tmp_path / "selection.json"
    selection.write_text("{}")
    (tmp_path / "selection.sha256").write_text(sha256(selection))
    selection.write_text('{"changed": true}')
    with pytest.raises(ValueError, match="edited"):
        check_frozen(ROOT, tmp_path)


def test_evaluation_marker_blocks_repeat_before_fit(tmp_path):
    (tmp_path / "evaluation_started.json").write_text("{}")
    with patch("nox_project.experiments.check_frozen", return_value={}):
        with pytest.raises(FileExistsError):
            evaluate(ROOT, tmp_path)


def test_report_from_synthetic_saved_results_without_fitting(tmp_path):
    from nox_project.reporting import make_report

    names = ["ols", "random_forest", "gradient_boosting", "mlp", "ridge", "lasso", "forward_ols"]
    (tmp_path / "evaluation_complete.json").write_text("{}")
    choices = {name: {"n_features": 9} for name in names}
    (tmp_path / "selection.json").write_text(json.dumps({"selected": choices}))
    path = [{"n_features": k, "validation": {"rmse": 10 / k}} for k in range(1, 10)]
    (tmp_path / "forward_path.json").write_text(json.dumps(path))
    candidates = [
        {"model": name, "params": {"alpha": alpha}, "train": {"rmse": 1}, "validation": {"rmse": 2}}
        for name in ["ridge", "lasso"]
        for alpha in [0.1, 1]
    ]
    (tmp_path / "candidates.json").write_text(json.dumps(candidates))
    pd.DataFrame([{"model": name, "mae": 1, "rmse": 2, "r2": 0.5} for name in names]).to_csv(
        tmp_path / "test_metrics.csv", index=False
    )
    pred = {TARGET: np.arange(20), **{name: np.arange(20) + 1 for name in names}}
    pd.DataFrame(pred).to_csv(tmp_path / "test_predictions.csv", index=False)
    make_report(tmp_path)
    assert len(list((tmp_path / "report").glob("*.png"))) == 12
    assert len(list((tmp_path / "report").glob("*.csv"))) == 4
