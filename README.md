# ME276DS — Gas Turbine NOx Emission Prediction

Reproducible preparation for the Fall 2026 group final project. **Code and data are ready; no models have been trained and no prediction results are claimed.**

We estimate hourly NOx concentration for power-plant operators and environmental monitoring engineers. The question is which course-relevant model balances prediction error, input count, and complexity. This is an analytical soft-sensor study, not a replacement for certified emissions monitoring or a causal study of emissions control.

## Scope and course alignment

The instructor asks for a tabular dataset, a real-world narrative, and comparison of modeling techniques learned in class. This project has 36,733 records and 9 predictors, satisfying the suggested minimums of 500 samples and 8 inputs. The raw CSVs total 2,778,809 bytes (~2.78 MB). The research plan defines three connected experiments:

| Experiment | Implemented methods | Question |
|---|---|---|
| 1: Main comparison | OLS, Random Forest, Gradient Boosting, MLP | How much does nonlinear modeling improve prediction? |
| 2: Feature selection | Greedy forward OLS selection; all-9-input OLS reference | Can a smaller input subset retain accuracy? |
| 3: Regularization | OLS, Ridge (L2), Lasso (L1) | How do penalties affect errors and coefficients? |

See [requirements and course mapping](docs/course_alignment.md) and the [original project plan](docs/ME276DS_Gas_Turbine_NOx_Project_Plan.pdf). Classification/logistic regression, CNN/RNN, SVM, and generative models are not added merely because they appear in the syllabus; the target is continuous and the approved scope is focused.

## Dataset and the updated split

Source: [UCI dataset 551](https://archive.ics.uci.edu/dataset/551/gas+turbine+co+and+nox+emission+data+set), [DOI 10.24432/C5WC95](https://doi.org/10.24432/C5WC95), **CC BY 4.0**. Five original CSVs are included in `data/raw/`, with source URL, retrieval date, sizes, counts and SHA-256 hashes in `data/manifest.json`. No CSV values were modified. Attribution and the variable dictionary are in [data/README.md](data/README.md).

Predictors: `AT, AP, AH, AFDP, GTEP, TIT, TAT, TEY, CDP`. Target: `NOX` (mg/m³). `CO`, year, and row ID are excluded from model inputs. Year is inferred from the filename. The released rows are chronological but do not contain timestamps: a row index is **not** an exact date or a guaranteed uninterrupted hourly timeline.

**User revision on 2026-10-29 takes precedence over the original PDF:**

| Partition | Records | Rows |
|---|---|---:|
| Training | All 2011–2014 records | 29,349 |
| Validation | First 3,692 records of 2015, original order | 3,692 |
| Test | Last 3,692 records of 2015, original order | 3,692 |

Within the CSV, these correspond to data rows 1–3,692 and 3,693–7,384 (excluding the header). All model fitting, including final refitting, uses **2011–2014 only**. Validation selects hyperparameters and features; test is used only after choices are frozen. The two 2015 blocks never overlap. This differs from the original plan/UCI paper protocol (2011–2013 development, 2014–2015 test), so our eventual scores must not be presented as a reproduction of that protocol.

## Install and verify without training

Python 3.11–3.13; verified environment is Python 3.12 on the A6000 host. The implementation uses CPU scikit-learn; an A6000 GPU is not needed for this tabular project. Each fit uses one CPU thread and Random Forest uses `n_jobs=1` to avoid consuming shared resources unexpectedly.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
bash scripts/check_no_training.sh
```

The check script compiles/imports code, runs lint and tests, verifies data hashes/schema/counts, records a training-only descriptive summary, and prints the experiment plan. **It never fits a model.** Test figures use synthetic saved arrays, never learned predictions. On systems lacking `ensurepip`, install the OS venv support or bootstrap pip inside the isolated venv; do not alter a shared Python environment. `requirements-lock.txt` records the verified Linux environment, including transitive dependencies; for exact recreation, install that file and then `pip install --no-deps -e .`.

Individual preparation commands, from the repository root:

```bash
nox download                     # offline checksum verification if data already exists
nox audit --output reports/data_audit.json
nox dry-run
```

`download` restores missing CSVs from the pinned archive and rejects changed existing files. `audit` checks all files structurally, but descriptive statistics are calculated on training years only. `dry-run` reports **73 development fits** (28 model-grid candidates + 45 forward-selection candidates) and 7 final refits; it does not execute them.

## Future experiments — do not run during preparation

Training is an explicit opt-in. The following commands are documented for a later authorized run and **have not been executed**:

```bash
source .venv/bin/activate
nox develop --run runs/main-s276 --execute
# Inspect validation results and convergence warnings before opening the test set.
nox evaluate --run runs/main-s276 --execute
nox report --run runs/main-s276
```

Without `--execute`, `develop` and `evaluate` fail before fitting. Development refuses an existing run directory. Final evaluation verifies the frozen selection, code fingerprint, data manifest and dependency versions, then creates an exclusive evaluation marker. It refuses a second evaluation of the same run. This protects against accidental reuse; it cannot prevent deliberate repeated testing in different run directories. After inspecting test results, do not tune models on them. If a run fails, retain its partial logs and marker, diagnose the failure and document any recovery instead of deleting the marker casually. Model files use joblib and should only be loaded from trusted runs.

## Modeling choices

- **Selection metric:** validation RMSE, to penalize occasional large emission-estimation errors. Report MAE for typical absolute error and R² for explained variation, alongside RMSE. Errors are in original mg/m³. No regulatory exceedance threshold has been supplied, so this is not an exceedance classifier.
- **Scaling:** per-fit `StandardScaler` pipelines for linear/penalized models and MLP. MLP also standardizes the target inside `TransformedTargetRegressor`, with inverse transformation before scoring. Tree ensembles use raw inputs. No preprocessing is fitted before splitting.
- **MLP:** Adam, ReLU, seed 276; no random early-stopping validation split. Architecture and L2 strength are selected against the chronological validation block; maximum 500 iterations. Convergence warnings are saved for review, not suppressed as evidence of successful convergence.
- **Forward selection:** start empty, add the remaining feature with lowest validation RMSE, evaluate subset sizes 1–9, choose the smallest subset within 1% of the best validation RMSE. This predeclared tolerance is a simplicity preference, not a significance test. Repeated adaptive reuse makes validation scores optimistic; only the untouched test block assesses generalization. This study applies to OLS, not claims of universally optimal sensors for all models.
- **Regularization:** alpha grids are explicit in `configs/experiments.json`. Standardized-input coefficients are saved; Ridge and Lasso objectives use different numerical alpha scales, so equal alpha values are not directly equivalent strengths.
- **Fairness:** shared split, predictors, seed and metrics; a mean-only baseline is not substituted for the planned linear baseline. Record fit time and number of inputs with accuracy. No outlier deletion, random row split, target transformation fitted on all years, or timestamp reconstruction.

## Outputs and project layout

```text
src/nox_project/    data, models, experiments, metrics, reporting, CLI
configs/           declared hyperparameter grids and seed
data/raw/          five original UCI CSVs (tracked in Git)
data/manifest.json pinned checksums and provenance
docs/              course requirements, original plan, methodology
tests/             data/split/guard/metric/report checks without training
reports/           preparation audit and verification record only
runs/              future experiments, models and figures (Git-ignored)
Agent_doc/         project maintenance and handoff notes
```

Future run outputs include candidate training/validation metrics and fit warnings, a forward-selection path, frozen choices, environment/Git provenance, seven serialized estimators, test predictions with original row IDs, MAE/RMSE/R², three experiment tables, prediction/residual plots, feature-count and penalty curves, and linear coefficients. They are **not present yet**. See [methodology and report checklist](docs/methodology.md) for interpretation limits and the remaining course deliverables.

## Current status

Prepared code, raw data, reproducible environment, and non-training checks. No training, tuning, final evaluation, performance conclusions, final report or presentation has been completed. The instructor's mid-November GSI meeting, RRR-week report and finals-week presentation remain course milestones; exact report/presentation deadlines are not invented here.
