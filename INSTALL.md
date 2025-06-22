# AiCode Installation Guide

## Quick Install

### Method 1: Automated Installer (Recommended)

1. Download and extract the AiCode package:
   ```bash
   # Extract the aicode-20250622.zip file
   unzip aicode-20250622.zip
   cd aicode-extracted/
   ```

2. Run the installer:
   ```bash
   # Interactive installation
   python3 install.py
   
   # Or automated installation
   python3 install.py --auto
   ```

3. The installer will:
   - Check Python and pip availability
   - Install all required dependencies
   - Set up AiCode in your home directory
   - Create launcher scripts and shell aliases
   - Test the installation

### Method 2: Manual Installation

1. Extract the package to your desired location:
   ```bash
   unzip aicode-20250622.zip -d ~/aicode
   cd ~/aicode
   ```

2. Install dependencies:
   ```bash
   pip3 install click rich requests pillow prompt-toolkit
   ```

3. Test the installation:
   ```bash
   python3 main.py --help
   ```

## Usage After Installation

### Start AiCode Interactive Shell
```bash
# If installer created alias (restart terminal first)
aicode

# Or use direct command
python3 ~/aicode/main.py
```

### Common Commands
```bash
# List available models
aicode models

# Configure settings
aicode configure

# Ask a single question
aicode ask "write a function to sort a list"

# Show help
aicode --help
```

## Configuration

### First Time Setup

1. Start your local model server (Ollama, LM Studio, etc.)

2. Configure AiCode to connect to your model:
   ```bash
   aicode configure
   ```

3. Or manually edit `~/aicode/config.ini`:
   ```ini
   [models]
   default = http://localhost:8080/v1/chat/completions
   ollama = http://localhost:11434/api/chat
   lmstudio = http://localhost:1234/v1/chat/completions
   ```

### Supported Model Servers

- **Ollama**: Default port 11434
- **LM Studio**: Default port 1234  
- **Any OpenAI-compatible API**: Custom endpoints

## Troubleshooting

### Installation Issues

**Python version error:**
- Requires Python 3.7 or higher
- Update Python or use pyenv/conda

**Permission errors:**
- Use `--user` flag: `pip3 install --user ...`
- Or install in virtual environment

**Missing dependencies:**
- Run: `pip3 install click rich requests pillow prompt-toolkit`

### Runtime Issues

**Model connection failed:**
- Ensure your local model server is running
- Check the endpoint URL in configuration
- Verify firewall/network settings

**Command not found:**
- Source your shell profile: `source ~/.bashrc`
- Use full path: `python3 ~/aicode/main.py`

**Import errors:**
- Ensure all files were extracted properly
- Check Python path includes installation directory

## Uninstallation

To remove AiCode:

1. Delete the installation directory:
   ```bash
   rm -rf ~/aicode
   ```

2. Remove shell aliases from `~/.bashrc`, `~/.zshrc`, or `~/.profile`:
   ```bash
   # Remove lines containing "alias aicode="
   ```

3. Optionally remove Python packages:
   ```bash
   pip3 uninstall click rich requests pillow prompt-toolkit
   ```

## Advanced Setup

### Custom Installation Directory

```bash
python3 install.py
# Enter custom path when prompted
```

### Virtual Environment Installation

```bash
python3 -m venv aicode-env
source aicode-env/bin/activate
python3 install.py --auto
```

### System-wide Installation

```bash
sudo python3 install.py --auto
# Installs to /opt/aicode or /usr/local/aicode
```

## Package Contents

The AiCode package includes:
- `main.py` - Entry point
- `install.py` - Installation script
- `config.ini` - Default configuration
- `aicode.md` - System context
- `README.md` - Documentation
- `aicode/` - Main package directory

## Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Review the aicode.md context file for capabilities
3. Ensure your local model server is properly configured