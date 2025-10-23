# Longitudinal Analysis Pipeline

A lightweight, script-centric pipeline for longitudinal statistical analysis using Python and R.

## Quick Start

### Prerequisites

1. **Python 3.10+** - Download from [python.org](https://python.org)
2. **R 4.0+** - Download from [CRAN](https://cran.r-project.org/)
   - Ubuntu/Debian: `sudo apt-get install r-base`
   - macOS: `brew install r`
   - Windows: Download and run the installer

### Installation

You have three options for setting up the environment:

#### Option 1: Complete Setup with Virtual Environment (Recommended)

**Linux/macOS:**
```bash
./create_venv.sh
```

**Windows:**
```cmd
create_venv.bat
```

This will:
- Create a Python virtual environment in `venv/` directory
- Activate the virtual environment
- Install all Python dependencies into the virtual environment
- Install required R packages
- Verify the installation

**After setup, always activate the virtual environment before working:**
```bash
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

#### Option 2: Automated Setup (Existing Virtual Environment)

First create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Then run:
```bash
python setup_environment.py
```

This script will:
- Check that you're in a virtual environment
- Install all Python dependencies into the virtual environment
- Install required R packages
- Verify the installation

#### Option 3: Manual Installation

1. **Create and activate virtual environment (required):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Python packages:**
```bash
pip install -r requirements.txt
```

3. **Install R packages:**
```bash
Rscript -e "install.packages(c('lme4', 'lmerTest', 'emmeans', 'MASS'), repos='https://cran.r-project.org/')"
```

4. **Install Quarto (optional, for reporting):**
   - Download from [quarto.org](https://quarto.org)

## Project Structure

```
longitudinal_analysis/
│
├── data/
│   ├── raw/           # Original CSV files
│   └── processed/     # Intermediate and final data files
│
├── scripts/           # Analysis scripts (run in numerical order)
│   ├── 01_load_and_validate.py
│   ├── 02_handle_outliers.py
│   ├── 03_impute_missing_data.py
│   ├── 04_generate_eda_report.ipynb
│   ├── 05_power_analysis.py
│   ├── 06_run_batch_modeling.py
│   ├── 07_run_batch_diagnostics.py
│   ├── 08_extract_and_correct_results.py
│   ├── 09_run_sensitivity_analysis.py
│   ├── 10_report_template.qmd
│   └── 11_run_batch_reporting.py
│
├── models/            # Fitted model objects
├── reports/           # Generated reports and figures
├── docs/              # Documentation
├── requirements.txt   # Python dependencies
├── setup_environment.py  # Automated setup script
├── create_venv.sh     # Linux/macOS virtual environment setup
├── create_venv.bat    # Windows virtual environment setup
└── README.md          # This file
```

## Usage

1. **Activate your virtual environment:**
```bash
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

2. Place your raw CSV files in `data/raw/`

3. Run the analysis scripts in numerical order:

```bash
# Start the analysis pipeline
python scripts/01_load_and_validate.py
python scripts/02_handle_outliers.py
python scripts/03_impute_missing_data.py
# ... continue with remaining scripts
```

4. Each script processes the output of the previous script
5. Inspect intermediate files in `data/processed/` as needed
6. Final reports will be generated in `reports/`

**Important:** Always work within the virtual environment to ensure you're using the correct packages and versions.

## Dependencies

### Python Core
- pandas: Data manipulation
- polars: Fast data processing
- scikit-learn: Machine learning utilities
- statsmodels: Statistical models
- seaborn/matplotlib: Visualization
- openpyxl: Excel file support
- pyarrow: Parquet file support
- jupyter: Interactive notebooks

### R Integration
- rpy2: Python-R interface
- pymer4: Python interface to R's lme4

### R Packages
- lme4: Linear mixed-effects models
- lmerTest: p-values for LMMs
- emmeans: Estimated marginal means
- MASS: GLMM utilities

## Troubleshooting

### R Installation Issues
- Ensure R is in your system PATH
- On Windows, you may need to add R to PATH manually
- On macOS, you might need to run `sudo ln -s /usr/local/bin/R /usr/bin/R`

### rpy2 Issues
- Make sure R and Python architectures match (both 64-bit)
- On Windows, install Rtools if not already present

### Package Conflicts
- It's recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Documentation

See `docs/roadmap.md` for detailed implementation guidance and statistical methodology.

## License

[Add your license information here]