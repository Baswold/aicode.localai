#!/usr/bin/env python3
"""
Final verification test for AiCode package
"""

import os
import sys
import tempfile
import zipfile
import subprocess

def test_package_complete():
    """Test that package contains all necessary files"""
    package_file = "aicode-20250622.zip"
    
    if not os.path.exists(package_file):
        print(f"Package file {package_file} not found")
        return False
    
    required_files = [
        "main.py",
        "install.py",
        "config.ini", 
        "aicode.md",
        "README.md",
        "INSTALL.md",
        "aicode/__init__.py",
        "aicode/cli.py",
        "aicode/config.py",
        "aicode/models.py",
        "aicode/shell.py",
        "aicode/tools.py",
        "aicode/prompts.py",
        "aicode/image_analyzer.py"
    ]
    
    with zipfile.ZipFile(package_file, 'r') as zf:
        package_contents = zf.namelist()
        
        missing_files = []
        for required_file in required_files:
            if required_file not in package_contents:
                missing_files.append(required_file)
        
        if missing_files:
            print(f"Missing files: {missing_files}")
            return False
        
        print(f"Package contains all {len(required_files)} required files")
        print(f"Total package size: {os.path.getsize(package_file)} bytes")
        return True

def test_installer_help():
    """Test installer help functionality"""
    try:
        import subprocess
        result = subprocess.run([sys.executable, "install.py", "--help"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "Usage:" in result.stdout:
            print("Installer help works correctly")
            return True
        else:
            print("Installer help failed")
            return False
    except Exception as e:
        print(f"Installer help test error: {e}")
        return False

def test_main_syntax():
    """Test main application syntax"""
    try:
        import subprocess
        result = subprocess.run([sys.executable, "-m", "py_compile", "main.py"], 
                              capture_output=True, timeout=10)
        if result.returncode == 0:
            print("Main application syntax is valid")
            return True
        else:
            print("Main application syntax error")
            return False
    except Exception as e:
        print(f"Syntax test error: {e}")
        return False

def main():
    """Run final verification tests"""
    print("Running final AiCode package verification...")
    print("=" * 50)
    
    tests = [
        test_package_complete,
        test_installer_help, 
        test_main_syntax
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("✓ PASS")
            else:
                print("✗ FAIL")
        except Exception as e:
            print(f"✗ ERROR: {e}")
        print("-" * 30)
    
    print(f"Final Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nPackage verification SUCCESSFUL!")
        print("AiCode is ready for distribution.")
        return True
    else:
        print(f"\nPackage verification FAILED!")
        print("Fix issues before distribution.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)