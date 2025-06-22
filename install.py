#!/usr/bin/env python3
"""
AiCode Installer
Installs AiCode CLI coding assistant with all dependencies
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✓ pip is available")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error: pip is not available")
        return False

def install_dependencies():
    """Install required Python packages"""
    dependencies = [
        "click",
        "rich", 
        "requests",
        "pillow",
        "prompt-toolkit"
    ]
    
    print("📦 Installing dependencies...")
    for dep in dependencies:
        try:
            print(f"  Installing {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                          check=True, capture_output=True)
            print(f"  ✓ {dep} installed")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Failed to install {dep}: {e}")
            return False
    
    print("✓ All dependencies installed successfully")
    return True

def extract_aicode(install_dir):
    """Extract AiCode files to installation directory"""
    print(f"📁 Creating installation directory: {install_dir}")
    os.makedirs(install_dir, exist_ok=True)
    
    # Copy current AiCode files
    files_to_copy = [
        "main.py",
        "config.ini", 
        "aicode.md",
        "README.md"
    ]
    
    aicode_dir = os.path.join(install_dir, "aicode")
    os.makedirs(aicode_dir, exist_ok=True)
    
    # Copy aicode package
    if os.path.exists("aicode"):
        print("  Copying aicode package...")
        shutil.copytree("aicode", aicode_dir, dirs_exist_ok=True)
        print("  ✓ aicode package copied")
    
    # Copy main files
    for file in files_to_copy:
        if os.path.exists(file):
            print(f"  Copying {file}...")
            shutil.copy2(file, install_dir)
            print(f"  ✓ {file} copied")
    
    return True

def create_launcher_script(install_dir):
    """Create launcher script for easy access"""
    launcher_content = f"""#!/usr/bin/env python3
import sys
import os

# Add AiCode installation directory to path
install_dir = "{install_dir}"
sys.path.insert(0, install_dir)

# Change to installation directory
os.chdir(install_dir)

# Import and run AiCode
from aicode.cli import main

if __name__ == "__main__":
    main()
"""
    
    launcher_path = os.path.join(install_dir, "aicode-launcher.py")
    with open(launcher_path, "w") as f:
        f.write(launcher_content)
    
    # Make executable on Unix systems
    if os.name != 'nt':
        os.chmod(launcher_path, 0o755)
    
    print(f"✓ Launcher script created: {launcher_path}")
    return launcher_path

def create_shell_alias(install_dir, launcher_path):
    """Create shell alias for easy access"""
    alias_command = f"alias aicode='python3 {launcher_path}'"
    
    shell_configs = [
        os.path.expanduser("~/.bashrc"),
        os.path.expanduser("~/.zshrc"),
        os.path.expanduser("~/.profile")
    ]
    
    for config_file in shell_configs:
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    content = f.read()
                
                if "alias aicode=" not in content:
                    with open(config_file, "a") as f:
                        f.write(f"\n# AiCode CLI Assistant\n{alias_command}\n")
                    print(f"✓ Added alias to {config_file}")
                else:
                    print(f"✓ Alias already exists in {config_file}")
            except Exception as e:
                print(f"⚠️  Could not modify {config_file}: {e}")

def test_installation(install_dir):
    """Test the installation"""
    print("🧪 Testing installation...")
    
    # Test import
    try:
        original_cwd = os.getcwd()
        os.chdir(install_dir)
        sys.path.insert(0, install_dir)
        
        from aicode.cli import main
        print("✓ AiCode imports successfully")
        
        # Test help command
        import subprocess
        result = subprocess.run([sys.executable, "main.py", "--help"], 
                              capture_output=True, text=True, cwd=install_dir)
        
        if result.returncode == 0 and "AiCode" in result.stdout:
            print("✓ Help command works")
        else:
            print("❌ Help command failed")
            return False
            
        # Test models command
        result = subprocess.run([sys.executable, "main.py", "models"], 
                              capture_output=True, text=True, cwd=install_dir)
        
        if result.returncode == 0:
            print("✓ Models command works")
        else:
            print("❌ Models command failed")
            return False
        
        os.chdir(original_cwd)
        sys.path.remove(install_dir)
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False
    
    print("✓ Installation test passed")
    return True

def main():
    """Main installer function"""
    print("🚀 AiCode CLI Assistant Installer")
    print("=" * 40)
    
    # Handle command line arguments
    if '--help' in sys.argv or '-h' in sys.argv:
        print("Usage: python install.py [--auto|--yes]")
        print("  --auto, --yes: Run in non-interactive mode")
        sys.exit(0)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_pip():
        sys.exit(1)
    
    # Check for non-interactive mode
    non_interactive = '--auto' in sys.argv or '--yes' in sys.argv
    
    # Get installation directory
    default_install_dir = os.path.expanduser("~/aicode")
    
    if non_interactive:
        install_dir = default_install_dir
        print(f"Auto-installing to: {install_dir}")
    else:
        try:
            install_dir = input(f"Installation directory (default: {default_install_dir}): ").strip()
            if not install_dir:
                install_dir = default_install_dir
        except (EOFError, KeyboardInterrupt):
            install_dir = default_install_dir
            print(f"Using default directory: {install_dir}")
    
    install_dir = os.path.abspath(install_dir)
    
    # Confirm installation
    print(f"\nInstallation Summary:")
    print(f"  Directory: {install_dir}")
    print(f"  Python: {sys.executable}")
    
    if non_interactive:
        print("Proceeding with auto-installation...")
    else:
        try:
            confirm = input("\nProceed with installation? (y/N): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print("Installation cancelled")
                sys.exit(0)
        except (EOFError, KeyboardInterrupt):
            print("\nUsing default confirmation (yes)")
            pass
    
    print("\n🔄 Starting installation...")
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed")
        sys.exit(1)
    
    # Extract files
    if not extract_aicode(install_dir):
        print("❌ File extraction failed")
        sys.exit(1)
    
    # Create launcher
    launcher_path = create_launcher_script(install_dir)
    
    # Create shell alias
    create_shell_alias(install_dir, launcher_path)
    
    # Test installation
    if not test_installation(install_dir):
        print("❌ Installation test failed")
        sys.exit(1)
    
    print("\n" + "=" * 40)
    print("✅ AiCode installation completed successfully!")
    print("\nUsage:")
    print(f"  Direct: python3 {launcher_path}")
    print(f"  Shell alias: aicode (after restarting terminal)")
    print(f"  Manual: cd {install_dir} && python3 main.py")
    print("\nTo get started:")
    print("  1. Start your local model server (Ollama, LM Studio, etc.)")
    print("  2. Run 'aicode configure' to set up your model endpoints")
    print("  3. Run 'aicode' to start the interactive shell")
    print("\nDocumentation: README.md in installation directory")

if __name__ == "__main__":
    main()