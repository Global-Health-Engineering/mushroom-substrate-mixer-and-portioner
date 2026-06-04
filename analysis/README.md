---
title: "README for `./analysis`"
output: pdf_document
---

This folder contains derived data. For details see the `README.pdf` file in the `../data` folder.

# Scripts Overview — Data Processing Pipeline

This directory contains the Python scripts used to process raw experimental data and generate all derived datasets and figures for the thesis *“Product Development of a Substrate Mixer and Portioning Device”*.

The scripts implement a fully reproducible workflow: all results, tables, and plots can be regenerated from the raw data without manual intervention.

---

## 1. `01_build_derived_data.py`

### Purpose
Processes all raw CSV files from `/data/raw_data` and produces a single tidy, long‑format dataset containing all measurements and derived variables from the first‑series experiments.

### Key Functions
- Load all raw CSV files (01.01, 01.02, 01.03, …)
- Reshape wide tables into long format
- Compute derived variables (e.g., water content, deviations, standard deviations)
- Standardize units and variable names
- Add metadata columns (test_id, trial, measurement_id, position, n_csr)
- Validate numeric ranges and missing values
- Write the final dataset to: /data/derived_data/

---

## 2. `02_generate_plots.py`

### Purpose
Generates all publication‑ready figures used in the thesis based on the combined derived dataset.

### Key Functions
- Load `derived_data.csv`
- Filter data by test (01.01, 01.02, 01.03)
- Produce line plots, boxplots, scatter plots, and distribution plots
- Apply consistent LaTeX‑ready styling (serif fonts, 300 dpi)
- Save figures to: /media/plots/


---

## Reproducibility

Running these two scripts in sequence fully regenerates:

- all derived data  
- all plots  
- all numerical results used in the thesis  

This ensures complete reproducibility and transparency of the data‑analysis workflow.



