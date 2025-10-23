@echo off
REM Virtual Environment Setup Script for Longitudinal Analysis (Windows)
REM This script creates a virtual environment and sets up the complete project

echo 🚀 Setting up Longitudinal Analysis Environment
echo ==============================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://python.org
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✓ Python version: %python_version%

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing Python packages...
pip install -r requirements.txt
echo ✓ Python packages installed

REM Check if R is installed
R --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  R is not installed or not in PATH
    echo Please install R from https://cran.r-project.org/bin/windows/base/
    echo.
    echo After installing R, run:
    echo   venv\Scripts\activate.bat
    echo   Rscript -e "install.packages(c('lme4', 'lmerTest', 'emmeans', 'MASS'), repos='https://cran.r-project.org/')"
) else (
    echo ✓ R is installed
    for /f "tokens=3" %%i in ('R --version 2^>^&1 ^| findstr /r "^R version"') do set r_version=%%i
    echo   R version: %r_version%
    
    REM Install R packages
    echo Installing R packages...
    Rscript -e "install.packages(c('lme4', 'lmerTest', 'emmeans', 'MASS'), repos='https://cran.r-project.org/', quiet=TRUE)"
    echo ✓ R packages installed
)

REM Verify installation
echo.
echo Verifying installation...
python setup_environment.py

echo.
echo 🎉 Setup complete!
echo.
echo To activate the environment in the future, run:
echo   venv\Scripts\activate.bat
echo.
echo To start the analysis, run:
echo   python scripts\01_load_and_validate.py
echo.
pause