### Experiment Setup

The experiment is a longitudinal study designed to evaluate the effects of two treatments (A and B) on multiple medical measurements over time. It is structured to capture dynamic changes in participant responses, accounting for individual variability, batch effects from replicates, and hierarchical nesting of data. The primary goal is to fully characterize treatment effects without reducing the data (e.g., avoiding summarization or averaging), enabling a comprehensive analysis of how treatments influence outcomes across time points.

#### Key Components of the Experiment Design:
- **Replicates**: There are 4 replicates (also referred to as batches or runs). Each replicate represents an independent iteration of the experiment, potentially conducted under similar but not identical conditions (e.g., different lab runs or time periods). This replication helps account for batch-to-batch variability, such as environmental or procedural differences. Replicates are treated as random effects in the analysis to generalize findings beyond these specific runs, unless they represent unique fixed conditions.
  
- **Participants**: Each replicate includes 8 participants, resulting in a total sample size of 32 participants (4 replicates × 8 participants). Participants are nested within replicates, meaning they are unique to each replicate and not shared across them. This nesting reflects the hierarchical structure of the data.

- **Treatment Assignment**: Within each replicate, participants are assigned to one of two treatments: Treatment A or Treatment B. The assignment is assumed to be randomized and approximately balanced (e.g., roughly 4 participants per treatment per replicate). Any imbalances are addressed in the analysis via covariates, such as baseline measurements, to control for potential biases.

- **Time Points**: Measurements are collected at 8 distinct time points (labeled as Time 1 through Time 8). These are longitudinal repeated measures, capturing changes over time within the same participants. There may also be a baseline measurement (Time 0) for each outcome, which is used as a covariate to adjust for initial differences and regression to the mean. Time can be treated as either continuous (for modeling linear or polynomial trends) or categorical (for time-specific comparisons).

- **Measurements/Outcomes**: Multiple medical measurements (outcome variables) are collected at each time point for each participant. These are not specified by name but are implied to be continuous (e.g., physiological metrics like blood pressure or biomarker levels) or potentially non-continuous (e.g., binary or count data if non-normal). The analysis is conducted separately for each outcome to avoid aggregation and to fully characterize treatment effects. The number of outcomes is configurable (listed in a YAML file), and they may vary in distribution (normal vs. skewed, over-dispersed counts, etc.).

- **Hierarchical and Longitudinal Nature**: The design is hierarchical: repeated measures (time points) are nested within participants, who are nested within replicates. This creates correlated data due to within-participant dependencies over time and potential batch effects across replicates. The experiment assumes good randomization, approximate balance, and missing data under the Missing at Random (MAR) assumption, with sensitivity checks for other patterns.

- **Objectives and Hypotheses**: The focus is on detecting treatment effects, particularly dynamic ones (e.g., how treatments diverge over time via Treatment × Time interactions). This includes overall effects, time-specific differences, and within-treatment changes from baseline. The setup allows for assessing heterogeneity (e.g., individual trajectories via random slopes) and robustness to data issues like outliers or missing values.

- **Data Sources**: Raw data comes from four separate CSV files (one per replicate), stored in `data/raw/`. These are concatenated during preprocessing to form a single dataset for analysis.

This setup maximizes statistical power by leveraging the full longitudinal structure, while incorporating robustness checks (e.g., for non-normality, missing data, or outliers) to ensure defensible inferences.

### Expected Dataset Structure

The dataset is expected to be in a **long format** (also known as tidy or panel data format), which is optimal for longitudinal analysis. This means each row represents a single observation (one measurement at one time point for one participant), rather than a wide format where time points are columns. The structure facilitates modeling repeated measures and hierarchical nesting.

#### Key Characteristics:
- **File Format and Sources**: Initially, four separate CSV files (e.g., `replicate_1.csv`, `replicate_2.csv`, etc.) in `data/raw/`. These are read-only and immutable. After loading and validation, they are concatenated into a single processed file (e.g., Parquet format for efficiency) in `data/processed/`.
  
- **Rows (Observations)**: Approximately 32 participants × 8 time points × number of outcomes, but since outcomes are analyzed separately, the core dataset focuses on participant-time combinations. With baselines, this could include an extra time point per participant.

- **Columns (Variables)**: The dataset includes identifiers for hierarchy, treatment, time, outcomes, and potentially derived flags (e.g., for outliers). All data is version-controlled and reproducible via scripts.

#### Detailed Column Structure:
Based on the descriptions, the expected columns in the consolidated long-format dataset are as follows (types and purposes inferred from the plans):

- **Replicate_ID** (Factor/String, e.g., "Rep1", "Rep2", "Rep3", "Rep4"):
  - Identifies the replicate (batch) for each observation.
  - Purpose: Models batch effects as random intercepts to account for variability across replicates.
  - Nested: Participants are unique within replicates.

- **Participant_ID** (Factor/String, e.g., "P001", "P002", ..., unique across or within replicates):
  - Unique identifier for each participant.
  - Purpose: Models individual heterogeneity via random intercepts and slopes (e.g., baseline differences and time trajectories).
  - Nested within Replicate_ID.

- **Treatment** (Factor/String, e.g., "A" or "B"):
  - Indicates the assigned treatment group.
  - Purpose: Fixed effect in models to compare A vs. B.

- **Time** (Integer or Numeric, e.g., 1 to 8; potentially 0 for baseline):
  - The time point of the measurement.
  - Purpose: Fixed effect (continuous for trends or categorical for specific points) in models. Interacted with Treatment for dynamic effects.
  - Note: Time is repeated within participants.

- **Baseline** (Numeric, optional):
  - The value of the outcome at Time 0 (pre-treatment).
  - Purpose: Covariate to adjust for initial differences between groups.

- **Outcome_Variable(s)** (Numeric, one or more columns, e.g., "Measurement_X", "Measurement_Y"):
  - The actual medical measurement values (e.g., continuous metrics like lab results).
  - Purpose: Dependent variables in models. Analyzed separately per outcome. May include multiple columns if outcomes are stored together, but typically processed one at a time.
  - Distributions: Assumed normal for LMMs; checked for non-normality (e.g., skewed → GLMM with Gamma; counts → Poisson/Negative Binomial).

- **Derived/Flagged Columns** (Added during preprocessing, Boolean or Numeric):
  - E.g., "Measurement_X_is_outlier" (Boolean): Flags potential outliers via methods like Isolation Forest.
  - Purpose: For sensitivity analyses (e.g., excluding outliers).

#### Example Dataset Snippet (Hypothetical Long Format):
| Replicate_ID | Participant_ID | Treatment | Time | Baseline | Measurement_X | Measurement_Y | Measurement_X_is_outlier |
|--------------|----------------|-----------|------|----------|---------------|---------------|---------------------------|
| Rep1        | P001          | A        | 1    | 5.2     | 5.5          | 10.2         | False                    |
| Rep1        | P001          | A        | 2    | 5.2     | 6.1          | 11.0         | False                    |
| ...         | ...           | ...      | ...  | ...     | ...          | ...          | ...                      |
| Rep1        | P008          | B        | 8    | 4.8     | 7.3          | 12.5         | True                     |
| Rep2        | P009          | A        | 1    | 5.0     | 5.4          | 9.8          | False                    |
| ...         | ...           | ...      | ...  | ...     | ...          | ...          | ...                      |

- **Total Rows**: For one outcome, ~256 (32 participants × 8 time points), plus baselines if separate.
- **Handling Missing Data**: Some cells in outcome columns may be NA (e.g., due to dropout). Imputed via MICE into multiple datasets for analysis.
- **Storage and Processing**: Raw CSVs → Validated Parquet (efficient, columnar). Intermediate files for imputed versions (e.g., multiple Parquet files for MICE sensitivity).

This structure ensures the data is ready for mixed-effects modeling, where correlations within participants and replicates are explicitly handled. All transformations (e.g., imputation, outlier flagging) are scripted and reproducible, with validations to catch issues early.