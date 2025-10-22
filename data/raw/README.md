# Sham Longitudinal Dataset Documentation

## Overview
This directory contains sham CSV files simulating a longitudinal medical experiment with 4 replicates, 8 participants each, evaluating two treatments (A and B) across 8 time points plus baseline.

## File Structure
- `replicate_1.csv` - 8 participants (P001-P008)
- `replicate_2.csv` - 8 participants (P009-P016) 
- `replicate_3.csv` - 8 participants (P017-P024)
- `replicate_4.csv` - 8 participants (P025-P032)

## Dataset Specifications

### Participants & Design
- **Total Participants**: 32 (8 per replicate)
- **Treatments**: A (standard care) vs B (new treatment)
- **Time Points**: 0 (baseline) through 8 (follow-up)
- **Design**: Balanced randomization (~4 participants per treatment per replicate)

### Measurements
- **Blood_Pressure_Systolic** (mmHg): 90-210 range, treatment should reduce over time
- **Heart_Rate** (bpm): 50-98 range, moderate treatment effect
- **Cholesterol_LDL** (mg/dL): 70-215 range, treatment reduces levels
- **Glucose_Fasting** (mg/dL): 68-162 range, treatment affects glucose control
- **BMI**: 25.1-37.5 range, relatively stable with minor changes
- **Inflammation_Marker** (CRP mg/L): 1.4-10.5 range, treatment reduces inflammation

### Real-World Features
- **Missing Data**: Simulated Missing at Random (MAR) patterns
- **Outliers**: Extreme blood pressure values marked in notes
- **Batch Effects**: Subtle systematic differences between replicates
- **Individual Variability**: Different baseline values and response patterns
- **Treatment Effects**: 
  - Treatment A: Moderate improvement (~10-15% reduction)
  - Treatment B: Better improvement (~20-30% reduction)
  - Effects increase over time (dynamic treatment × time interaction)

### Column Descriptions
- `Replicate_ID`: Batch identifier (Rep1-Rep4)
- `Participant_ID`: Unique participant identifier
- `Treatment`: A or B
- `Time`: 0-8 (0 = baseline, 1-8 = follow-up)
- `Blood_Pressure_Systolic`: Systolic blood pressure
- `Heart_Rate`: Beats per minute
- `Cholesterol_LDL`: LDL cholesterol levels
- `Glucose_Fasting`: Fasting glucose
- `BMI`: Body mass index
- `Inflammation_Marker`: C-reactive protein
- `Notes`: Annotations for missing data or outliers

## Intended Use
These files are designed to test:
- Longitudinal mixed-effects modeling
- Missing data imputation (MICE)
- Outlier detection and handling
- Batch effect correction
- Treatment × time interaction analysis
- Statistical power analysis

## Data Quality
- Total observations: 288 rows (32 participants × 9 time points)
- Missing data rate: ~3-5% (MAR pattern)
- Outlier rate: ~1-2% (marked in notes)
- Treatment balance: Approximately 50/50 within each replicate

This dataset provides a realistic foundation for implementing and testing the statistical analysis pipeline described in the project roadmap.