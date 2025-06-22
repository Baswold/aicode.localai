# AiCode - CLI Coding Assistant

## Overview
AiCode is a resource-efficient CLI coding assistant optimized for small local models. It provides an interactive shell with full tool execution capabilities, model switching, and image analysis.

## Core Features

### 🤖 Model Management
- Support for multiple local model endpoints (Ollama, LM Studio, OpenAI-compatible)
- Easy model switching during runtime
- Connection testing and status monitoring
- Optimized prompts for small models with limited context

### 🛠️ Tool Execution System
- File operations (read, write, create, delete, list directories)
- Terminal command execution with safety checks
- Code analysis and syntax error detection
- Basic code formatting capabilities
- Safe mode with user confirmation for dangerous operations

### 🖼️ Image Analysis
- Visual debugging and understanding capabilities
- Image optimization for small models
- Basic visual analysis (colors, dimensions, complexity)
- Image comparison functionality
- Text region detection (basic implementation)

### 💬 Interactive Shell
- Rich CLI interface with syntax highlighting
- Command completion and history
- Context management and conversation tracking
- Debug mode for troubleshooting
- Multiple prompt optimization strategies

## Configuration

### Model Endpoints
- **Default**: `http://localhost:8080/v1/chat/completions`
- **Ollama**: `http://localhost:11434/api/chat`
- **LM Studio**: `http://localhost:1234/v1/chat/completions`
- **Custom**: Any OpenAI-compatible endpoint

### Settings
- **Max Tokens**: 2048 (optimized for small models)
- **Temperature**: 0.7
- **Context Length**: 4096 tokens
- **Timeout**: 30 seconds
- **Safe Mode**: Enabled by default

## Tool Categories

### File Operations
- `read_file(path)` - Read file content with syntax highlighting
- `write_file(path, content)` - Write content to file
- `list_directory(path)` - List directory contents
- `create_directory(path)` - Create directories
- `delete_file(path)` - Delete files (with confirmation)
- `file_exists(path)` - Check file existence

### Terminal Operations
- `execute_command(command)` - Run shell commands safely
- `get_working_directory()` - Get current directory
- `change_directory(path)` - Change working directory

### Code Analysis
- `analyze_code(code, language)` - Analyze code structure and metrics
- `find_syntax_errors(code, language)` - Detect syntax errors
- `format_code(code, language)` - Basic code formatting

## Command Reference

### Shell Commands
- `/help` - Show available commands
- `/models` - List configured models with status
- `/switch <model>` - Switch to different model
- `/tools` - Show available tools
- `/clear` - Clear conversation history
- `/history` - Show recent conversation
- `/context` - Show current context
- `/image <path>` - Analyze image file
- `/debug` - Enter debug mode
- `/analyze <file>` - Analyze code file
- `/exit` or `/quit` - Exit AiCode

### Usage Patterns
- **Natural conversation**: Ask coding questions directly
- **Explicit tool calls**: Use `TOOL: tool_name(param="value")` syntax
- **File analysis**: `/analyze filename.py`
- **Image debugging**: `/image screenshot.png`
- **Model switching**: `/switch ollama`

## Optimization for Small Models

### Prompt Engineering
- Compressed context management
- Specialized system prompts for different tasks
- Context truncation to fit token limits
- Efficient message formatting

### Performance Features
- Image size optimization for vision models
- Code analysis without external dependencies
- Minimal memory footprint
- Fast response processing

## Safety Features

### Safe Mode
- Confirmation prompts for dangerous operations
- File path validation
- Command filtering for destructive operations
- User consent for system-level changes

### Error Handling
- Graceful failure recovery
- Detailed error messages
- Connection retry logic
- Input validation

## Context Management

### Conversation History
- Stores recent user-assistant exchanges
- Automatic context compression
- Relevant context injection
- Session persistence

### File Context
- Code file analysis results
- Image analysis metadata
- Tool execution outcomes
- Working directory tracking

## Supported Languages

### Primary Support
- Python (full AST analysis)
- JavaScript/TypeScript
- HTML/CSS
- JSON/YAML

### Basic Support
- Shell scripts
- Configuration files
- Text files
- Log files

## Integration Points

### Local Model Servers
- **Ollama**: Direct API integration
- **LM Studio**: OpenAI-compatible endpoint
- **Custom servers**: Any OpenAI-format API

### Development Workflow
- Code analysis and review
- Error debugging and fixing
- File management and organization
- Terminal command execution

## Best Practices

### For Small Models
- Keep prompts concise and focused
- Use specific, targeted questions
- Leverage tool execution for complex tasks
- Break down large problems into smaller steps

### For Safety
- Always enable safe mode in production
- Review file operations before execution
- Use relative paths when possible
- Backup important files before modifications

### For Efficiency
- Switch models based on task complexity
- Use image analysis for visual debugging
- Leverage conversation history for context
- Use specific commands for common tasks

## Error Recovery

### Common Issues
- Model connection failures
- File permission errors
- Syntax errors in code
- Tool execution timeouts

### Recovery Strategies
- Automatic retry with exponential backoff
- Fallback to basic functionality
- User notification and guidance
- Graceful degradation

## Extensibility

### Adding New Tools
1. Implement tool function in `tools.py`
2. Add to tool initialization
3. Update help documentation
4. Test with safety checks

### Adding New Models
1. Add endpoint to configuration
2. Test connection and compatibility
3. Optimize prompts if needed
4. Update model management

This context provides comprehensive information about AiCode's capabilities, configuration, and usage patterns to help the AI assistant understand and work effectively within the system.