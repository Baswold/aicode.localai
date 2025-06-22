#!/usr/bin/env python3
"""
Compact AiCode Installer
Simple installer for the single-file AiCode system
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_dependencies():
    """Install required packages"""
    packages = ["rich", "prompt-toolkit", "requests", "pillow"]
    
    print("Installing required packages...")
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✓ {package}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")
            return False
    return True

def create_executable():
    """Create executable script"""
    if os.name == 'nt':  # Windows
        script_name = "aicode.bat"
        script_content = f'@echo off\npython "{os.path.abspath("aicode_compact.py")}" %*'
    else:  # Unix-like
        script_name = "aicode"
        script_content = f'#!/bin/bash\npython3 "{os.path.abspath("aicode_compact.py")}" "$@"'
    
    try:
        with open(script_name, 'w') as f:
            f.write(script_content)
        
        if os.name != 'nt':
            os.chmod(script_name, 0o755)
        
        print(f"✓ Created {script_name}")
        return script_name
    except Exception as e:
        print(f"✗ Failed to create executable: {e}")
        return None

def create_default_files():
    """Create default configuration files"""
    files_created = []
    
    # Create aicode.md if it doesn't exist
    if not os.path.exists("aicode.md"):
        with open("aicode.md", 'w') as f:
            f.write("""# AiCode Context

This file contains context information for your AiCode assistant.

## Project Description
Add your project description here...

## Key Files
- List important files in your project
- Explain their purpose

## Current Tasks
- What you're working on
- What needs to be done

## Notes
- Any important notes or reminders
- Coding patterns or preferences
""")
        files_created.append("aicode.md")
    
    return files_created

def main():
    """Main installer function"""
    print("AiCode Compact Installer")
    print("=" * 30)
    
    # Check if aicode_compact.py exists
    if not os.path.exists("aicode_compact.py"):
        print("✗ aicode_compact.py not found in current directory")
        return 1
    
    # Install dependencies
    if not install_dependencies():
        print("✗ Failed to install dependencies")
        return 1
    
    # Create executable
    executable = create_executable()
    if not executable:
        return 1
    
    # Create default files
    created_files = create_default_files()
    for file in created_files:
        print(f"✓ Created {file}")
    
    print("\n🎉 Installation complete!")
    print(f"\nUsage:")
    print(f"  ./{executable}")
    print(f"  python3 aicode_compact.py")
    
    print(f"\nNext steps:")
    print(f"1. Start your local model server (Ollama, LM Studio, etc.)")
    print(f"2. Run: ./{executable}")
    print(f"3. Use '/config' to check settings")
    print(f"4. Edit aicode.md to add project context")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())