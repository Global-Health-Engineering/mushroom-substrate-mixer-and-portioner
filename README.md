---
title: "README for `root`"
output: pdf_document
---

# Overview

This is the directory for the bachelor's thesis of Peter Siegenthaler (psiegenthale@ethz.ch), named "Product Development of a Substrate Mixer and Portioning Device" conducted at the Global Health Engineering research group at ETH Zurich. The folder contains a structure for generated data with guidance on how to store raw and derived data.


# Directories & Files

The repository has the following directory tree:

    .
    ├── README.md
    ├── analysis
    │   └── README.md
    ├── data
    │   ├── README.md
    │   ├── derived_data
    │   │   └── README.md
    │   ├── metadata
    │   │   ├── README.md
    │   │   └── codebook.csv
    │   │   └── file_list.csv
    │   └── raw_data
    │       └── README.md
    ├── docs
    │   ├── README.md
    │   ├── reports
    │   │   ├── bsc_thesis_psiegenthale.pdf
    │   │   ├── proposal_psiegenthale.pdf
    │   │   └── README.md
    │   └── slides
    │       ├── presentation_psiegenthale.pptx
    │       ├── presentation_psiegenthale.pdf
    │       └── README.md
    ├── grading
    │   └── README.md
    ├── hardware
    │   ├── README.md
    │   ├── design
    │   │   └── README.md
    │   └── testing
    │       └── README.md
    ├── media
    │   ├── README.md
    │   ├── photo
    │   │    └── README.md
    │   ├── video
    │   │    └── README.md
    │   └── correspondence
    │        └── README.md
    ├── src
    │   └── README.md
    └── tree.txt

| name         | description                                                                                                                                                                                                                        |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| README.pdf   | File to write up general information about this project.                                                                                                                                                                           |
| analysis     | Directory containing code for data analysis.                                                                                                                                                                 |
| data         | Data directory with sub-directories (raw_data, derived_data, metadata). This directory and its all sub-directories contain README.md files with instructions and information about their content.                                  |
| docs         | Directory for documents that are generated as part of the project. Two sub-folders (report and slides) provide the manuscript and the presentations prepared over the course of the project. |
| grading      | Directory containing template for grading the project and the student. Supervisors need to ensure that students are aware of this grading rubric prior to starting their work with the GHE group.                                  |
| hardware     | Directory containing hardware design, calculations and documentation as well as testing documentation as a product of the project.                                                                                                 |
| media        | Directory for storing media related to the project (divided into photo and video sub-directories).                                                                                                                                 |
| src          | Directory for software development (not analysis files)                                                                                                                                                                     |