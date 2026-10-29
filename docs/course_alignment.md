# Course requirements and precedence

Sources: instructor announcement and syllabus pasted by the user; supplied project plan PDF; supplied lecture PDFs. These documents provide task evidence, not authorization to email, submit forms, publish a website or launch training.

Precedence for this implementation:

1. Current explicit user instructions, including no training and the updated 2011–2014 / 2015 split.
2. Instructor project requirements.
3. Team project plan (three experiments, 9 inputs, NOX output).
4. Slides/syllabus as reference for modeling concepts.

| Requirement or source | Implementation / status |
|---|---|
| Dataset plus stakeholder narrative | UCI 551; plant operators and environmental monitoring engineers |
| At least 8 features, 500 samples; avoid very large files | 9 inputs, 36,733 rows, 2.78 MB original CSVs |
| Variety of course models | OLS, Random Forest, Gradient Boosting, MLP |
| Plan: feature selection and regularization | Forward OLS, Ridge, Lasso |
| Supervised learning slides, pp. 11–15 | MAE/RMSE/R², held-out evaluation, validation-based hyperparameter selection |
| Linear regression 1–2 | Linear baseline; engineering interpretation of coefficients with caution |
| Linear regression 3, pp. 3–11 | Overfitting, feature selection, Ridge/Lasso |
| Probability/optimization slides | Statistical assumptions and numerical optimization context |
| Classification and logistic regression slides | Reference only; not required for a continuous NOX target |
| Team size 3–5 | Administrative requirement; membership not supplied/modified |
| Mandatory workshop | Announcement says October 27; pasted calendar places workshop in Thursday column of Oct 26–30. This discrepancy is not resolved by code; no attendance claim made. |
| GSI check-in | 30-minute Zoom meeting in mid-November; exact slot not supplied |
| Report and presentation | RRR-week report (exact date/format TBD), finals-week presentation |
| Optional website | Not required by instructor; outside this implementation |

The supplied PDF remains unchanged as historical evidence. Its older held-out-year split is superseded by the user's explicit revision: training years 2011–2014; disjoint first/second halves of 2015 for validation/test. Workshop-form submissions, team registration, attendance, final report and presentation are not completed by preparing this repository.
