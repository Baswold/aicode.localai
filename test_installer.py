#!/usr/bin/env python3
"""
Test script for AiCode installer
"""

import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path

def test_package_extraction():
    """Test that the package extracts correctly"""
    print("Testing package extraction...")
    
    package_file = "aicode-20250622.zip"
    if not os.path.exists(package_file):
        print(f"❌ Package file {package_file} not found")
        return False
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract package
        result = subprocess.run([
            sys.executable, "-m", "zipfile", "-e", package_file, temp_dir
        ], capture_output=True)
        
        if result.returncode != 0:
            print("❌ Failed to extract package")
            return False
        
        # Check required files exist
        required_files = [
            "main.py",
            "install.py", 
            "config.ini",
            "aicode.md",
            "README.md",
            "aicode/__init__.py",
            "aicode/cli.py"
        ]
        
        for file in required_files:
            file_path = os.path.join(temp_dir, file)
            if not os.path.exists(file_path):
                print(f"❌ Missing required file: {file}")
                return False
        
        print("✓ Package extraction successful")
        return True

def test_basic_import():
    """Test that AiCode can be imported"""
    print("Testing basic import...")
    
    try:
        # Test in current directory
        from aicode.cli import main
        print("✓ AiCode imports successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_cli_commands():
    """Test basic CLI commands"""
    print("Testing CLI commands...")
    
    # Test help command
    result = subprocess.run([
        sys.executable, "main.py", "--help"
    ], capture_output=True, text=True)
    
    if result.returncode != 0 or "AiCode" not in result.stdout:
        print("❌ Help command failed")
        return False
    
    # Test models command  
    result = subprocess.run([
        sys.executable, "main.py", "models"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Models command failed")
        return False
    
    print("✓ CLI commands working")
    return True

def test_installer_syntax():
    """Test that installer script has valid syntax"""
    print("Testing installer syntax...")
    
    result = subprocess.run([
        sys.executable, "-m", "py_compile", "install.py"
    ], capture_output=True)
    
    if result.returncode != 0:
        print("❌ Installer syntax error")
        return False
    
    print("✓ Installer syntax valid")
    return True

def main():
    """Run all tests"""
    print("🧪 Testing AiCode Package and Installer")
    print("=" * 40)
    
    tests = [
        test_package_extraction,
        test_basic_import,
        test_cli_commands,
        test_installer_syntax
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    
    if failed == 0:
        print("✅ All tests passed! Package is ready for distribution.")
        return True
    else:
        print("❌ Some tests failed. Package needs fixes.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)