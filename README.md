# Gas Turbine NOₓ Prediction

2026fall-ME276DS · 276ds-group3

[![Open project website](https://img.shields.io/badge/Project_website-Open-175CD3?style=for-the-badge)](https://me276ds-turbine-nox.vigilantdrape.chatgpt.site/)
[![Open UCI dataset](https://img.shields.io/badge/UCI_dataset-Open-287A59?style=for-the-badge)](https://archive.ics.uci.edu/dataset/551/gas+turbine+co+and+nox+emission+data+set)

We estimate hourly NOₓ concentrations from routine gas turbine readings to help plant operators cross-check emission measurements and investigate unusual readings. The UCI dataset contains 36,733 hourly records from one power plant in northwestern Türkiye.

1. **Training windows.** We compare linear regression, random forest, gradient boosting, and an MLP on three training windows. The longest window gives the MLP a test RMSE of 8.070 mg/m³.
2. **MLP architecture.** An eight-unit hidden layer leads the four architecture variants with a test RMSE of 7.861 mg/m³.
3. **Feature selection.** Removing air filter differential pressure (AFDP) gives the lowest RMSE among the nine input removals, at 7.799 mg/m³.
4. **Regularization.** With the original seed, L2 strength α = 0.003 reduces RMSE from 7.781 to 7.646 mg/m³. Zero regularization performs slightly better with the two additional seeds.
