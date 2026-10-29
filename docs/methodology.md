# Experimental protocol and future write-up

## Frozen protocol

Use `2011–2014 → train`, first half of 2015 → validation, second half → test. The half-year wording is approximate: these are halves of the available ordered records, not known calendar dates. No shuffling across partitions. 2015 validation labels are never included in the fitted training set, including final refits.

All six model families train on the same 29,349 rows; four comprise the main comparison. Use the explicit candidate grids and seed in `configs/experiments.json`. Selection minimizes validation RMSE. Ties follow deterministic grid order. The forward OLS experiment uses the same validation block to choose additions and subset size; a 1% RMSE tolerance favors the smallest competitive subset. Its selected feature set can contain all nine inputs if reduction does not qualify.

Development logs training and validation scores, fit times and warnings per candidate; no test predictions are generated. `selection.json` freezes one choice per family and the forward OLS subset. Final evaluation rejects changed code, manifest, package versions or selection bytes, fits all seven selected configurations using training years only, and scores the second 2015 block. Reporting consumes saved outputs and never refits.

The holdout file is physically read for integrity checking and split construction because validation and test share one CSV. Only validation rows are passed to model/feature-selection routines; test values cannot enter fitting, scaling, ranking or descriptive training summaries. Structural QA is not test-set model evaluation.

## Leakage, uncertainty and interpretation

- Contiguous records may be correlated, including across the validation/test boundary. A temporal split reduces random-split optimism but does not make samples iid. No significance claims or iid confidence intervals are produced by default.
- Reusing validation for many candidates and greedy feature additions introduces selection optimism. Validation results guide selection; they are not unbiased final performance estimates.
- Different operating regimes and yearly shift may dominate results. The test only assesses a later period at the same plant; generalization to other plants is unknown.
- These are simultaneous measurements. The narrative is an estimate from already available operating measurements, not a future forecast or pre-operation optimization tool. TEY and other sensor availability must be checked for any deployment.
- Correlated inputs can yield unstable OLS/Lasso coefficients or interchangeable selected features. Penalized coefficients describe association; feature removal is a predictive experiment, not safety justification for removing instrumentation.
- Ridge minimizes squared error plus an L2 term; sklearn Lasso uses a sample-normalized squared error plus L1. Compare their own alpha curves, not raw alpha magnitudes across families.
- MLP optimization and Lasso convergence warnings must be reviewed on validation before final evaluation. A returned prediction does not establish convergence. No model run has yet been performed.
- Test metrics are for reporting, not another tuning signal. Re-running in a new directory after viewing the test does not restore its held-out status.

## Final report checklist (future work)

1. State stakeholder, intended use, data source/license, target and 9 inputs.
2. Explain revised chronological split, raw-data QA, preprocessing, seed and search grids.
3. Present four-model comparison: MAE, RMSE, R², fit time and qualitative complexity.
4. Present forward-selection curve, selected variables and all-input baseline comparison.
5. Present Ridge/Lasso penalty curves, coefficients and selected penalties against OLS.
6. Include prediction/residual plots and interpret large errors, temporal limitations, correlated sensors and optimization warnings.
7. State team contributions and conclusions supported by actual results. Avoid causal/regulatory claims.
8. Prepare presentation after report results exist; confirm instructor's final format/deadlines.

## Implementation references

- UCI dataset page and DOI linked in the main README (source chronology, license, variables).
- [scikit-learn 1.7 Pipeline](https://scikit-learn.org/1.7/modules/generated/sklearn.pipeline.Pipeline.html): encapsulated training-only preprocessing.
- [scikit-learn 1.7 MLPRegressor](https://scikit-learn.org/1.7/modules/generated/sklearn.neural_network.MLPRegressor.html): early stopping, regularization and optimization settings.
- Installed scikit-learn 1.7.2 parameter constraints are checked locally; source code is authoritative for the pinned runtime.
