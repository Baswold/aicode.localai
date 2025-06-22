# AiCode - CLI Coding Assistant

A resource-efficient CLI coding assistant optimized for small local models with full tool execution capabilities.

## Features

🤖 **Multi-Model Support**: Works with Ollama, LM Studio, and any OpenAI-compatible endpoint
🛠️ **Tool Execution**: File operations, terminal commands, code analysis, and image processing
🖼️ **Image Analysis**: Visual debugging and understanding capabilities
💬 **Interactive Shell**: Rich CLI interface with command completion and history
🔧 **Optimized for Small Models**: Efficient prompts and context management
🛡️ **Safety Features**: Safe mode with confirmation for dangerous operations

## Quick Start

### Installation
```bash
pip install click rich requests pillow prompt-toolkit
```

### Run AiCode
```bash
python main.py
```

### Basic Commands
```bash
# Start interactive shell
python main.py

# Configure settings
python main.py configure

# List available models
python main.py models

# Ask a single question
python main.py ask "write a function to sort a list"
```

## Configuration

Default model endpoints are configured in `config.ini`:
- **Ollama**: `http://localhost:11434/api/chat`
- **LM Studio**: `http://localhost:1234/v1/chat/completions`
- **Default**: `http://localhost:8080/v1/chat/completions`

## Interactive Shell Commands

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/models` | List configured models with status |
| `/switch <model>` | Switch to different model |
| `/tools` | Show available tools |
| `/clear` | Clear conversation history |
| `/image <path>` | Analyze image file |
| `/analyze <file>` | Analyze code file |
| `/debug` | Enter debug mode |
| `/exit` | Exit AiCode |

## Tool Capabilities

### File Operations
- Read/write files with syntax highlighting
- Directory listing and creation
- File deletion (with safety confirmation)
- Path validation and existence checking

### Terminal Operations
- Safe command execution with timeouts
- Working directory management
- Output capture and formatting

### Code Analysis
- Syntax error detection
- Code structure analysis
- Basic formatting capabilities
- Language-specific parsing (Python AST)

### Image Analysis
- Visual debugging support
- Image optimization for small models
- Basic visual analysis (colors, dimensions)
- Image comparison functionality

## Usage Examples

### Basic Conversation
```
aicode> write a function to calculate fibonacci numbers
```

### File Operations
```
aicode> read the file main.py and analyze it
aicode> TOOL: read_file(path="main.py")
```

### Image Analysis
```
aicode> /image screenshot.png
aicode> analyze this error screenshot
```

### Model Switching
```
aicode> /switch ollama
aicode> /models
```

## Safety Features

- **Safe Mode**: Enabled by default, asks for confirmation on dangerous operations
- **Path Validation**: Prevents unauthorized file access
- **Command Filtering**: Blocks potentially destructive terminal commands
- **Timeout Protection**: Prevents hanging operations

## Small Model Optimization

- **Context Compression**: Automatically truncates context to fit token limits
- **Specialized Prompts**: Optimized for coding, debugging, and analysis tasks
- **Efficient Processing**: Minimal memory footprint and fast response times
- **Image Optimization**: Resizes images for optimal model processing

## Configuration Options

```ini
[DEFAULT]
max_tokens = 2048
temperature = 0.7
context_length = 4096
timeout = 30

[models]
default = http://localhost:8080/v1/chat/completions
ollama = http://localhost:11434/api/chat
lmstudio = http://localhost:1234/v1/chat/completions

[tools]
enable_file_operations = true
enable_terminal_commands = true
enable_image_analysis = true
safe_mode = true
```

## Context Management

AiCode automatically loads system context from `aicode.md` which provides comprehensive information about capabilities and usage patterns. This enables the AI to understand its environment and provide better assistance.

## Development

The project structure is modular and extensible:

```
aicode/
├── __init__.py          # Package initialization
├── cli.py              # CLI interface and commands
├── config.py           # Configuration management
├── models.py           # Model communication
├── tools.py            # Tool execution system
├── prompts.py          # Prompt optimization
├── shell.py            # Interactive shell
└── image_analyzer.py   # Image processing
```

## Requirements

- Python 3.7+
- Local model server (Ollama, LM Studio, etc.)
- Terminal with basic cursor support

## License

Open source - feel free to modify and extend for your needs.