#!/bin/bash

# Virtual Environment Setup Script for Longitudinal Analysis
# This script creates a virtual environment and sets up the complete project

set -e  # Exit on any error

echo "🚀 Setting up Longitudinal Analysis Environment"
echo "=============================================="

# Check if Python 3.10+ is installed
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.10+ is required. Found version: $python_version"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

echo "✓ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt
echo "✓ Python packages installed"

# Check if R is installed
if command -v R &> /dev/null; then
    echo "✓ R is installed"
    r_version=$(R --version | head -n1 | awk '{print $3}')
    echo "  R version: $r_version"
    
    # Install R packages
    echo "Installing R packages..."
    Rscript -e "install.packages(c('lme4', 'lmerTest', 'emmeans', 'MASS'), repos='https://cran.r-project.org/', quiet=TRUE)"
    echo "✓ R packages installed"
else
    echo "⚠️  R is not installed or not in PATH"
    echo "Please install R first:"
    echo "  - Ubuntu/Debian: sudo apt-get install r-base"
    echo "  - macOS: brew install r"
    echo "  - Windows: Download from https://cran.r-project.org/"
    echo ""
    echo "After installing R, run:"
    echo "  source venv/bin/activate"
    echo "  Rscript -e \"install.packages(c('lme4', 'lmerTest', 'emmeans', 'MASS'), repos='https://cran.r-project.org/')\""
fi

# Verify installation
echo ""
echo "Verifying installation..."
python setup_environment.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To activate the environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start the analysis, run:"
echo "  python scripts/01_load_and_validate.py"