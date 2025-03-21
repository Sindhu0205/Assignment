# Assignment - Data Processor Validation
## Overview
This project validates the functionality of a Data Processor module. The Data processor module processes player data. `.csv` and `.json` are input files are read by the module and processed them based on predefined rules, and compares the output against expected results.

## Features
- Reads data from `.csv` (1990-2000) and `.json` (2000 onwards)
- Classification of players as **All-Rounder**, **Batsman**, or **Bowler**
- Filtering data based on appropriate age and missing data.
- Saving the results as `odi_results.csv` and `test_results.csv`
- Validates output and generates `test_result.csv`

## Repository Structure
```
📦 Assignment
├── inputDataSet/            # Input files (.csv & .json)
├── outputDataSet/           # Expected output files
├── assignment.py            # Main script
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
```

## Example Data Processing
**Input Data:**
```
eventType;playerName;age;runs;wickets
ODI;ABC123;25;1000;171
TEST;CDE456;45;100;100
ODI;EFG789;24;2500;10
```

**Processed Output:**
```
ODI;ABC123;25;1000;171;All-Rounder
TEST;CDE456;45;100;100;Bowler
ODI;HIJ012;10;250;29;Bowler
```

