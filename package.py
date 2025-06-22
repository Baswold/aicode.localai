#!/usr/bin/env python3
"""
AiCode Package Creator
Creates a distributable zip package of AiCode
"""

import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

def create_package():
    """Create AiCode zip package"""
    package_name = f"aicode-{datetime.now().strftime('%Y%m%d')}.zip"
    
    print(f"Creating package: {package_name}")
    
    # Files to include in package
    files_to_package = [
        "main.py",
        "config.ini", 
        "aicode.md",
        "README.md",
        "install.py",
        "INSTALL.md"
    ]
    
    # Directories to include
    dirs_to_package = [
        "aicode"
    ]
    
    with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add files
        for file in files_to_package:
            if os.path.exists(file):
                zipf.write(file)
                print(f"  Added: {file}")
        
        # Add directories
        for dir_name in dirs_to_package:
            if os.path.exists(dir_name):
                for root, dirs, files in os.walk(dir_name):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path)
                        zipf.write(file_path, arcname)
                        print(f"  Added: {arcname}")
    
    print(f"Package created: {package_name}")
    return package_name

if __name__ == "__main__":
    create_package()