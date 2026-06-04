# Derived Data README — Bachelor's Thesis Dataset  
**Substrate Mixer and Portioning Device**  
Global Health Engineering, ETH Zürich  
Author: Peter Siegenthaler  
June 2026

# Derived Data — Overview  
This directory contains all machine‑generated datasets produced by the reproducible analysis pipeline of the First-series and the test reports (PDF) of the Zero-series as described in `/data/metadata/README.md`.

----

# Zero‑Series Test Reports (PDF)

In addition to the machine‑generated first‑series datasets, this directory also contains the archived PDF reports of all zero‑series experiments (Test IDs 00.YY):

00_01_1_1_stability_supportingstructure_testreport.pdf
00_02_1_3_stability_friction_plainbearing_testreport.pdf
00_03_1_2_agitator_model_testreport.pdf
00_04_1_4_orifices_testreport.pdf

These documents summarize early‑stage prototype evaluations and contain qualitative observations, manual measurements, and exploratory findings.
Because zero‑series tests were not designed for computational analysis and do not follow the structured CSV schema, they are not included in the Python‑based processing pipeline.

They are stored here to ensure:

- complete archival of all experimental work
- transparent documentation of design decisions
- traceability between exploratory insights and the controlled first‑series experiments


----

## First-Series derived data (CSV)

All files in this folder are created exclusively by the script `01_build_derived_data.py` and contain tables of all first-series experiments (Test IDs 01.YY):

01_01_1_4_test_watercontent_derived.csv
01_02_1_3_test_portions_derived.csv
01_03_1_3_agitator_longitudinal_derived.csv
01_04_1_3_manifold_derived.csv

- cleaned and standardized measurement tables  
- all derived variables (mean, standard deviation, SEM, RSD, propagated errors)  
- theoretical reference values  
- quality‑check indicators  
- trial‑level annotations  

These files are the authoritative source for all numerical results and figures used in the thesis.  
No manual edits are applied at any stage.

----

For detailed descriptions of each test, see the metadata overview in /data/metadata/README.md

For a complete list of files, see `/data/metadata/file_list.csv`.  
For variable definitions, see `/data/metadata/codebook.csv`.

