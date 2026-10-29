# Dataset attribution and dictionary

Gas Turbine CO and NOx Emission Data Set [Dataset]. (2019). UCI Machine Learning Repository. https://doi.org/10.24432/C5WC95.

Source and download: https://archive.ics.uci.edu/dataset/551/gas+turbine+co+and+nox+emission+data+set

License: [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). The original five CSVs are redistributed without modification. No endorsement by the data contributors or UCI is implied. Derived metadata (`year`, `row_id`, partitions) are added only in memory. Source retrieval date: 2026-10-29; byte-level provenance is in `manifest.json`.

| Column | Meaning | Units as listed by UCI | Project role |
|---|---|---|---|
| AT | Ambient temperature | °C | input |
| AP | Ambient pressure | mbar | input |
| AH | Ambient humidity | % | input |
| AFDP | Air filter difference pressure | mbar | input |
| GTEP | Gas turbine exhaust pressure | mbar | input |
| TIT | Turbine inlet temperature | °C | input |
| TAT | Turbine after temperature | °C | input |
| TEY | Turbine energy yield | MWh | input |
| CDP | Compressor discharge pressure | mbar (UCI label) | input |
| CO | Carbon monoxide | mg/m³ | excluded |
| NOX | Nitrogen oxides | mg/m³ | target |

UCI lists CDP as mbar although its numerical scale warrants checking against the originating paper before physical interpretation. This project preserves source values and does not silently convert units. UCI's web schema includes `year`, while the actual CSVs have exactly 11 columns and no year column; the loader checks the real CSV schema.

The observations are hourly aggregates from one plant in northwestern Turkey, 2011–2015. Exact timestamps are absent; chronological order is preserved. Repeated measurement vectors are reported, not automatically dropped: no event IDs establish that they are erroneous duplicates. The audit found 7 repeated measurement rows in 2014 and none within the other annual files; all are retained. There are no missing/non-numeric values in the downloaded snapshot. Missing/corrupt files fail validation rather than being silently imputed.

The primary software has no license grant beyond the owner's repository permissions; the dataset's CC BY 4.0 terms apply independently to these files.
