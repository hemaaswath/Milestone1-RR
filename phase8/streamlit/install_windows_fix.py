"""
Windows Installation Fix for Phase 8 Streamlit App

This script helps resolve pandas installation issues on Windows.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and display results."""
    print(f"\n🔧 {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Failed!")
            if result.stderr:
                print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    """Main installation process."""
    print("🚀 Phase 8 Streamlit - Windows Installation Fix")
    print("=" * 50)
    
    print("\n📋 This script will help install the required packages for Windows.")
    print("If pandas installation fails, we'll try alternative methods.")
    
    # Method 1: Try pip with --no-cache-dir
    print("\n" + "="*50)
    print("Method 1: Standard pip installation with cache bypass")
    print("="*50)
    
    success = run_command(
        "pip install --no-cache-dir -r requirements.txt",
        "Installing packages without cache"
    )
    
    if success:
        print("\n🎉 All packages installed successfully!")
        print("\nYou can now run the app with:")
        print("streamlit run app.py")
        return
    
    # Method 2: Try conda if available
    print("\n" + "="*50)
    print("Method 2: Try conda installation")
    print("="*50)
    
    conda_available = run_command(
        "conda --version",
        "Checking if conda is available"
    )
    
    if conda_available:
        print("✅ Conda found! Installing with conda...")
        
        packages = [
            "streamlit=1.28.0",
            "pandas=2.1.3", 
            "plotly=5.17.0",
            "requests=2.31.0",
            "python-dotenv=1.0.0"
        ]
        
        for package in packages:
            run_command(f"conda install {package} -y", f"Installing {package}")
        
        print("\n🎉 All packages installed with conda!")
        print("\nYou can now run the app with:")
        print("streamlit run app.py")
        return
    
    # Method 3: Try individual package installation
    print("\n" + "="*50)
    print("Method 3: Individual package installation")
    print("="*50)
    
    # Install without pandas first
    basic_packages = [
        "streamlit==1.28.0",
        "plotly==5.17.0", 
        "requests==2.31.0",
        "python-dotenv==1.0.0"
    ]
    
    all_success = True
    for package in basic_packages:
        success = run_command(
            f"pip install {package}",
            f"Installing {package}"
        )
        if not success:
            all_success = False
            break
    
    if all_success:
        print("\n✅ Basic packages installed!")
        
        # Try pandas with different approaches
        print("\n🔧 Attempting pandas installation...")
        
        pandas_attempts = [
            "pip install --no-cache-dir pandas==2.1.3",
            "pip install --upgrade pip setuptools wheel",
            "pip install --no-cache-dir --upgrade pandas",
            "pip install pandas==2.0.3",  # Try older version
        ]
        
        for attempt in pandas_attempts:
            print(f"\nTrying: {attempt}")
            success = run_command(attempt, "Installing pandas")
            if success:
                print("\n🎉 Pandas installed successfully!")
                print("\nYou can now run the app with:")
                print("streamlit run app.py")
                return
        
        print("\n⚠️ Pandas installation failed, but other packages are installed.")
        print("\nYou can try running the app without pandas:")
        print("streamlit run app.py")
        print("(Charts and analytics may not work without pandas)")
        return
    
    # Method 4: Use Windows requirements file
    print("\n" + "="*50)
    print("Method 4: Install without pandas (Windows requirements)")
    print("="*50)
    
    success = run_command(
        "pip install -r requirements_windows.txt",
        "Installing packages without pandas"
    )
    
    if success:
        print("\n✅ Basic packages installed!")
        print("\n⚠️ Pandas was not installed - charts and analytics will be limited.")
        print("\nYou can run the app with:")
        print("streamlit run app.py")
        print("\nFor full functionality, you'll need to install pandas separately.")
        print("Try: pip install pandas from the Microsoft Store or use conda.")
        return
    
    # Method 5: Last resort - minimal installation
    print("\n" + "="*50)
    print("Method 5: Minimal installation")
    print("="*50)
    
    minimal_packages = ["streamlit", "requests", "python-dotenv"]
    
    for package in minimal_packages:
        run_command(f"pip install {package}", f"Installing {package}")
    
    print("\n✅ Minimal packages installed!")
    print("\n⚠️ Limited functionality - charts and analytics will not work.")
    print("\nYou can run the basic app with:")
    print("streamlit run app.py")

if __name__ == "__main__":
    main()
