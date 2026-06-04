# Metadata README — Bachelor's Thesis Dataset  
**Substrate Mixer and Portioning Device**  
Global Health Engineering, ETH Zürich  
Author: Peter Siegenthaler  
June 2026

## Overview
This repository contains all experimental data generated during the development and evaluation of a substrate mixer and portioning device. The data are organized according to academic data‑management standards and follow the structure recommended by ETH Library and Cornell University Research Data Management guidelines.

The dataset is divided into two major categories:

### 1. Zero‑Series Experiments (Test IDs 00.YY)
Zero‑series experiments represent early‑stage prototype and component‑level tests conducted during agile development.  
These tests primarily contain qualitative observations and a small number of manually recorded measurements.  
Because the data volume is low and not intended for computational analysis, zero‑series tests are provided as **human‑readable PDF reports** rather than machine‑readable CSV files.

### 2. First‑Series Experiments (Test IDs 01.YY)
First‑series experiments represent the full‑scale evaluation of the final prototype.  
These datasets contain structured, high‑quality measurements suitable for computational analysis.  
All first‑series tests are provided in **machine‑readable CSV format**, accompanied by:
- raw data (`/data/raw_data`)
- derived data (`/data/derived_data`)
- metadata and variable definitions (`/data/metadata/codebook.csv`)
- reproducible processing Python scripts (`/analysis`)
- list of all contained files for data analysis (`/data/metadata/file_list.csv`)

### File Naming Convention
Files follow the pattern:

`XX_YY_A_B_description_details.ext`

Where:
- `XX` = series (00 = zero‑series, 01 = first‑series)  
- `YY` = test ID  
- `A_B` = included trial numbers (e.g., `1_3` = trials 1–3; `1_1` = only trial 1)  
- `description` = short test descriptor  
- `details` = optional additional information  



---------------------------------------------------------------------------------------------------


### Test 00.01 — Stability of Supporting Structure  
Source: 00_01_1_1_stability_supportingstructure_testreport.pdf

This test evaluated the static and dynamic stability of the supporting structure designed to hold the oil barrel during mixer operation. The objective was to verify that the frame resists tilting under operational loads, including the dead weight of the barrel, substrate loads exceeding 100 L, and torques generated during manual agitation.

Tilting moments were measured using an analog force gauge at defined application points along the longitudinal and radial axes. Restoring moments were calculated from the total system weight and geometry. Stability factors exceeded 1.0 in all directions (Slong = 1.28, Srad = 1.21), confirming sufficient structural stability.

The test was exploratory and qualitative in nature; therefore, results are archived as a PDF report rather than machine‑readable data.


---------------------------------------------------------------------------------------------------
### Test 00.02 — Stability and Friction of Plain Bearing  
Source: 00_02_1_3_stability_friction_plainbearing_testreport.pdf

This experiment assessed the feasibility of a low‑cost wooden radial plain bearing for supporting the steel drive shaft of the manual agitator. The hypothesis was that wood provides adequate structural stability and sufficiently low friction (µ < 0.3) for low‑frequency manual operation.

Tangential forces at the crank lever were measured using a spring scale, and friction coefficients were calculated from the resulting torque. Two conditions were tested: the initial bore and a post‑boring modification. The modified configuration achieved µ ≈ 0.36, supported by qualitative evidence such as improved coast‑down behavior (6–7 revolutions after a single impulse).

Due to low data volume and the qualitative nature of the evaluation, results are provided as a PDF report rather than machine‑readable CSV files.


---------------------------------------------------------------------------------------------------
### Test 00.03 — Agitator Model Scale 1:5 Mixing Homogeneity  
Source: 00_03_1_2_agitator_model_testreport.pdf

This test compared two prototype agitator geometries (V1: T‑paddle, V2: V‑paddle) using a 1:5 scale model to evaluate mixing efficiency, axial transport, and operational stability. Two substrate loading scenarios were tested: uniform distribution and localized center loading.

Mass ratios of coffee and chives were sampled at multiple crankshaft rotations (CSR). Both prototypes achieved visual homogeneity under uniform loading, while axial transport remained limited under localized loading. V2 mixed slightly faster but caused substrate ejection due to a “shovel effect,” whereas V1 demonstrated more stable operation.

Given the exploratory nature and limited measurement precision (±1 g), results are archived as a PDF report rather than machine‑readable data.


---------------------------------------------------------------------------------------------------

Test 00.04 — Orifices / Water Distribution System Performance
Source: 00_04_1_4_orifices_testreport.pdf

This test evaluated the hydraulic performance of the water‑distribution manifold used to inject moisture into the substrate mixer. The objective was to understand how nozzle diameter, hydraulic head, and the number of orifices influence volumetric flow uniformity along the manifold.

Four experimental configurations were tested, ranging from 5‑hole to 11‑hole layouts, with hydraulic heads between 15 cm and 120 cm. Flow volumes were collected manually using graduated cylinders. For the 11‑hole configuration, adjacent nozzles were grouped into shared measurement vessels due to spatial constraints.

High sensitivity to micro‑scale manufacturing defects at 1 mm bore diameter.
Stochastic flow distribution rather than a predictable pressure‑drop gradient.
Sufficient hydraulic capacity of the manifold even at low heads (15 cm).
Need for systematic diameter enlargement to reduce clogging sensitivity and increase throughput.

Theoretical analysis suggests an ideal bore diameter of ~1.70 mm for uniform distribution under design conditions (Δh = 0.4 m, Q = 4 L/min)

Because this test was exploratory and relied on grouped measurements and qualitative observations, results are archived as a PDF report rather than machine‑readable CSV files. The insights informed the design of the controlled first‑series manifold tests (Test 01.04).

---------------------------------------------------------------------------------------------------

## Data Processing and Reproducibility Strategy for First‑Series Experiments (Test IDs 01.YY)

All first‑series experiments (Test IDs 01.YY) follow a fully reproducible, script‑based data‑processing workflow. The goal is to ensure transparency, traceability, and long‑term usability of the dataset in accordance with ETH Zürich and international research‑data standards.

### Raw Data
Raw data are stored as machine‑readable CSV files in `/data/raw_data`. These files contain only directly measured values without any manual corrections, formulas, or derived quantities.

### Derived Data
All derived variables (e.g., water content, standard deviations, deviations from mean values, homogeneity metrics) are computed programmatically using Python. No derived values are stored manually or calculated in spreadsheet software. The output of the processing pipeline is a single tidy, long‑format dataset: /data/derived_data/derived_data.csv

This file contains all measurements and derived variables from all first‑series experiments in a unified schema.

### Processing Pipeline
Two Python scripts located in `/analysis` implement the full computational workflow:

1. **01_build_derived_data.py**  
   Reads all raw CSV files, reshapes them into long format, computes all derived variables, and writes the combined `derived_data.csv`.

2. **01_generate_plots.py**  
   Reads `derived_data.csv` and generates all publication‑ready figures used in the thesis (PNG format, LaTeX‑compatible).

This structure ensures that all results and figures can be regenerated at any time from the raw data alone.

### Metadata and Codebook
All variables used in both raw and derived datasets are documented in `/data/metadata/codebook.csv`.  
The codebook defines variable names, types, units, ranges, and descriptions following general metadata standards (schema.org‑inspired).

This approach guarantees that the dataset is self‑describing, interoperable, and suitable for open‑data publication.

---------------------------------------------------------------------------------------------------


### Test 01.01 — Water Content Distribution During Mixing  
Source: 01_01_1_4_watercontent_raw.csv

This experiment investigates how uniformly water is distributed within the substrate during mixing. Measurements were taken manually at four paddle positions at multiple time points (0–10 minutes). For each time point, wet mass (m_wet) and dry mass (m_dry) were recorded. All other quantities (m_water, water content w, standard deviations, deviations from mean values) are derived computationally.

Three full trials were conducted, with a fourth trial prepared as a placeholder for future measurements.

Raw data include only directly measured values and observational notes. All derived variables are computed programmatically in the data‑processing pipeline.

### Substrate Composition (Trial‑Level Metadata)

The following substrate parameters were used in Test 01.01.  
Values for Trial 4 are placeholders and will be updated once measurements are available.

| Trial | m_sawdust_kg | m_straw_kg | m_water_kg | m_total_kg | w_theory |
|--------|--------|--------------------|---------------------|-------|-------|
| 1     | 19.01 | 7.11 | 52.24  | 78.36  | 0.667 |
| 2     | 8.01  | 2.11 | 20.24  | 30.36  | 0.667 |
| 3     | 8.00  | 4.50 | 17.472 | 29.952 | 0.682 |
| 4     | 4.36  | 2.12 | 16.03  | 22.51  | 0.651 |


---------------------------------------------------------------------------------------------------

### Test 01.02 — Portioning Homogeneity  
Source: 01_02_2_4_portions_raw.csv

This experiment evaluates the homogeneity of substrate portioning using the filling line. Individual bag masses (m_bag) were measured for each portion. Additionally, for every fifth bag (1, 5, 10, 15, …), wet and dry probe masses (m_probe_wet, m_probe_dry) were recorded to determine water content within the portions.

Two prototypes were tested:
- **V3, Conveyor Line PE-Tube ** in Trial 1  
- **V4, Conveyor Line Diffusor** in Trial 2 and 3  

Raw data include only directly measured values. All derived variables (e.g., water content, mass deviation, standard deviations, homogeneity metrics) are computed programmatically in the data‑processing pipeline.

Observational notes from the operator are included in the raw data file where relevant.


---------------------------------------------------------------------------------------------------
## Test 01.03 - Agitator Longitudinal Transport
Source: 01_03_1_3_agitator_longitudinal_raw.csv

This dataset contains measurements of substrate transport along the longitudinal axis of the mixer. 
Measurements were taken manually at four paddle positions after 0, 5, and 10 crankshaft rotations. 
Two experimental conditions were tested: substrate placed in the center (test_id 1.1) and substrate placed at the vessel edges (test_id 1.2). 
Three independent trials were performed for each condition.

Raw data include only directly measured fill levels and experimental settings. 
Derived data include calculated standard deviations and deviations from the mean fill level. 


---------------------------------------------------------------------------------------------------

## Test 01.04 - Manifold Water Flow
Source: 01_04_1_3_manifold_raw.csv

This dataset contains measurements of volumetric water flow through the orifices of the water‑distribution manifold. Measurements were taken manually at each orifice position under different experimental configurations. The tested conditions include varying numbers of active orifices and different bore diameters.

For each configuration, three independent trials were performed.

Raw data include only directly measured flow volumes and experimental settings.  
Derived data include calculated orifice diameters, pressure gradients, standard deviations, and deviations from the mean flow rate.

### Test 01.04 — Experimental Conditions Overview

| Test ID | Trials | Hydraulic Head [m] | Bore Diameter [mm] | Notes |
|--------|--------|--------------------|---------------------|-------|
| 5 | 1–2 | 0.4 | 2.0 | Early prototype, uneven flow distribution |
| 6 | 1–3 | 0.4 | 2.5 | Orifice 11 partially blocked in Trial 2; cleared in Trial 3 |
| 7 | 1–3 | 0.4 | 3.0 | Bore enlarged to 3 mm; significantly higher total flow |

### Note on Tests 1–5 (Exploratory Phase)

Tests 1–5 of the manifold development were executed in an exploratory manner and relied heavily on personal observations to identify design weaknesses and optimization potential. These tests were essential for understanding system behavior but were not performed under controlled or repeatable conditions. Therefore, the data from Tests 1–5 are not included in the Python‑based analysis pipeline and are archived only as qualitative development notes.


