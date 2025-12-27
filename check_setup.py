"""
Diagnostic script to check if everything is set up correctly.
Run this before starting the application.
"""
import sys
import os

def check_python_version():
    """Check if Python version is 3.11+"""
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("  ⚠ WARNING: Python 3.11+ is recommended")
        return False
    return True

def check_imports():
    """Check if all required modules can be imported"""
    modules = {
        'streamlit': 'streamlit',
        'google.genai': 'google-genai',
        'google.generativeai': 'google-generativeai',
        'dotenv': 'python-dotenv',
        'watchdog': 'watchdog'
    }
    
    print("\nChecking required modules:")
    all_ok = True
    for module_name, package_name in modules.items():
        try:
            __import__(module_name)
            print(f"  ✓ {package_name} - OK")
        except ImportError:
            print(f"  ✗ {package_name} - MISSING (install with: pip install {package_name})")
            all_ok = False
    
    return all_ok

def check_files():
    """Check if all required files exist"""
    required_files = [
        'main.py',
        'auth.py',
        'document_store.py',
        'team_store.py',
        'gemini_utils.py',
        'create_team.py'
    ]
    
    print("\nChecking required files:")
    all_ok = True
    for filename in required_files:
        if os.path.exists(filename):
            print(f"  ✓ {filename} - Found")
        else:
            print(f"  ✗ {filename} - MISSING")
            all_ok = False
    
    return all_ok

def check_directories():
    """Check if required directories exist or can be created"""
    required_dirs = ['uploaded_docs']
    
    print("\nChecking directories:")
    all_ok = True
    for dirname in required_dirs:
        if os.path.exists(dirname):
            print(f"  ✓ {dirname}/ - Exists")
        else:
            try:
                os.makedirs(dirname, exist_ok=True)
                print(f"  ✓ {dirname}/ - Created")
            except Exception as e:
                print(f"  ✗ {dirname}/ - Cannot create: {e}")
                all_ok = False
    
    return all_ok

def check_team_store():
    """Check if team_store module works"""
    try:
        import team_store
        teams = team_store.get_teams()
        print(f"\n✓ team_store.py - Working ({len(teams)} team(s) found)")
        return True
    except Exception as e:
        print(f"\n✗ team_store.py - Error: {e}")
        return False

def check_streamlit_import():
    """Try importing streamlit and check version"""
    try:
        import streamlit as st
        print(f"\n✓ Streamlit can be imported")
        try:
            version = st.__version__
            print(f"  Streamlit version: {version}")
        except:
            pass
        return True
    except Exception as e:
        print(f"\n✗ Streamlit import failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Knowledge Transfer Hub - Setup Diagnostic")
    print("=" * 60)
    
    results = []
    
    # Run checks
    results.append(("Python Version", check_python_version()))
    results.append(("Required Modules", check_imports()))
    results.append(("Required Files", check_files()))
    results.append(("Directories", check_directories()))
    results.append(("Team Store", check_team_store()))
    results.append(("Streamlit Import", check_streamlit_import()))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All checks passed! You should be able to run the app.")
        print("\nNext step: Run 'streamlit run main.py'")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  1. Install missing modules: pip install <module-name>")
        print("  2. Make sure you're in the correct directory")
        print("  3. Activate your virtual environment if using one")
    print("=" * 60)

if __name__ == "__main__":
    main()

