"""
Environment Setup Script for Longitudinal Analysis

This script sets up the complete Python and R environment for the longitudinal analysis project.
It installs Python packages via pip and R packages via rpy2.

Usage:
    python setup_environment.py
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    print(f"Running: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("✓ Success")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def install_python_packages():
    """Install Python packages from requirements.txt."""
    print("\n=== Installing Python Packages ===")
    
    # Upgrade pip first
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                "Upgrading pip")
    
    # Install requirements
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                "Installing Python packages")
    
    return True

def install_r_packages():
    """Install R packages via rpy2."""
    print("\n=== Installing R Packages ===")
    
    r_packages = [
        "lme4",
        "lmerTest", 
        "emmeans",
        "MASS"  # For GLMM negative binomial
    ]
    
    # Create R script to install packages
    r_script = """
# Install required R packages
packages <- c({packages})

# Check if packages are installed
missing_packages <- packages[!(packages %in% installed.packages()[,"Package"])]

if(length(missing_packages) > 0) {{
    cat("Installing missing packages:", paste(missing_packages, collapse=", "), "\\n")
    install.packages(missing_packages, repos="https://cran.r-project.org/")
}} else {{
    cat("All R packages are already installed\\n")
}}

cat("Loading packages to verify installation...\\n")
for(pkg in packages) {{
    library(pkg, character.only=TRUE)
    cat("✓", pkg, "loaded successfully\\n")
}}
""".format(packages=", ".join([f'"{pkg}"' for pkg in r_packages]))
    
    # Write R script to temporary file
    with open("install_r_packages.R", "w") as f:
        f.write(r_script)
    
    # Run R script
    success = run_command(["Rscript", "install_r_packages.R"], 
                         "Installing R packages")
    
    # Clean up temporary file
    if os.path.exists("install_r_packages.R"):
        os.remove("install_r_packages.R")
    
    return success

def check_r_installation():
    """Check if R is properly installed."""
    print("\n=== Checking R Installation ===")
    
    # Check if R is available
    if not run_command(["R", "--version"], "Checking R version"):
        print("\n⚠️  R is not installed or not in PATH")
        print("Please install R first:")
        print("  - Ubuntu/Debian: sudo apt-get install r-base")
        print("  - macOS: brew install r")
        print("  - Windows: Download from https://cran.r-project.org/")
        return False
    
    return True

def verify_installation():
    """Verify that all key packages can be imported."""
    print("\n=== Verifying Installation ===")
    
    test_script = """
import sys

# Test Python packages
python_packages = ['pandas', 'polars', 'sklearn', 'statsmodels', 
                   'seaborn', 'matplotlib', 'openpyxl', 'pyarrow', 'jupyter']

for pkg in python_packages:
    try:
        __import__(pkg)
        print(f"✓ {pkg}")
    except ImportError as e:
        print(f"✗ {pkg}: {e}")
        sys.exit(1)

# Test rpy2 and R packages
try:
    import rpy2.robjects as ro
    from rpy2.robjects import pandas2ri
    from rpy2.robjects.conversion import localconverter
    
    # Use the new conversion context approach
    with localconverter(ro.default_converter + pandas2ri.converter):
        # Test R packages
        r_packages = ['lme4', 'lmerTest', 'emmeans', 'MASS']
        for pkg in r_packages:
            try:
                ro.r(f'library({pkg})')
                print(f"✓ R package: {pkg}")
            except Exception as e:
                print(f"✗ R package {pkg}: {e}")
                sys.exit(1)
                
        print("✓ rpy2 and R packages working correctly")
    
except ImportError as e:
    print(f"✗ rpy2: {e}")
    sys.exit(1)

print("\\n🎉 All packages installed and verified successfully!")
"""
    
    with open("verify_installation.py", "w") as f:
        f.write(test_script)
    
    success = run_command([sys.executable, "verify_installation.py"], 
                         "Verifying installation")
    
    # Clean up
    if os.path.exists("verify_installation.py"):
        os.remove("verify_installation.py")
    
    return success

def check_virtual_env():
    """Check if running in a virtual environment."""
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    return in_venv

def main():
    """Main setup function."""
    print("🚀 Setting up Longitudinal Analysis Environment")
    print("=" * 50)
    
    # Check if in virtual environment
    if not check_virtual_env():
        print("⚠️  Warning: Not running in a virtual environment")
        print("It's highly recommended to use a virtual environment:")
        print("  python -m venv venv")
        print("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("")
        
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled. Please create a virtual environment first.")
            sys.exit(0)
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("⚠️  Warning: Python 3.10+ is recommended")
        print(f"Current version: {sys.version}")
    
    # Install Python packages
    if not install_python_packages():
        print("❌ Failed to install Python packages")
        print("\nIf you got an 'externally-managed-environment' error:")
        print("1. Create a virtual environment: python -m venv venv")
        print("2. Activate it: source venv/bin/activate")
        print("3. Run this script again from within the virtual environment")
        sys.exit(1)
    
    # Check R installation
    if not check_r_installation():
        print("❌ R installation required")
        sys.exit(1)
    
    # Install R packages
    if not install_r_packages():
        print("❌ Failed to install R packages")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("❌ Installation verification failed")
        sys.exit(1)
    
    print("\n✅ Environment setup complete!")
    print("\nNext steps:")
    print("1. Activate your virtual environment if using one")
    print("2. Run the analysis scripts in order from the scripts/ directory")
    print("3. Start with: python scripts/01_load_and_validate.py")

if __name__ == "__main__":
    main()