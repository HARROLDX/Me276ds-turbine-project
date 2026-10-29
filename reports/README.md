# Preparation verification — 2026-10-29

Executed on the A6000 host in the isolated Python 3.12.3 environment:

```bash
bash scripts/check_no_training.sh
```

- 16 tests passed, including split integrity, input exclusions, nonfinite rejection, model cloning, CLI execution guards, frozen-selection checks, and figure generation from synthetic saved arrays.
- Ruff and byte compilation passed.
- Five original-file hashes match the manifest; all 36,733 records have the expected 11 numeric columns, with no missing/nonfinite cells.
- Training: 29,349; validation: 3,692; test: 3,692. Seven repeated measurement rows in 2014 were retained.
- Dry-run constructed the plan and fit counts without training.
- No real estimator.fit call, training run, evaluation, or learned-performance result was produced. Actual fit/optimization behavior is still unverified.

`verification.log` contains the command outputs. `data_audit.json` contains structural checks and training-years-only descriptive statistics. These are preparation artifacts, not final scientific results.
