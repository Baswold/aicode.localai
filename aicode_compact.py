#!/usr/bin/env python3
"""
AiCode - Compact CLI coding assistant for small local models
All-in-one file with complete functionality
"""

import os
import sys
import json
import ast
import re
import subprocess
import configparser
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

# Rich imports for UI
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.syntax import Syntax
    from rich.prompt import Prompt, Confirm
    from prompt_toolkit import prompt as toolkit_prompt
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.completion import WordCompleter
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "rich", "prompt-toolkit", "requests", "pillow"])
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.syntax import Syntax
    from rich.prompt import Prompt, Confirm
    from prompt_toolkit import prompt as toolkit_prompt
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.completion import WordCompleter

console = Console()

class CompactAiCode:
    def __init__(self):
        self.config = self._load_config()
        self.conversation_history = []
        self.context = []
        self.current_model = "default"
        self.theme = "default"
        self.sessions = {}
        self.debug_history = []
        self.plans = {}
        
        # Built-in themes
        self.themes = {
            "default": {"primary": "cyan", "success": "green", "warning": "yellow", "error": "red"},
            "dark": {"primary": "bright_magenta", "success": "bright_green", "warning": "bright_yellow", "error": "bright_red"},
            "ocean": {"primary": "bright_blue", "success": "bright_cyan", "warning": "bright_yellow", "error": "bright_red"}
        }
        
        # Load context if available
        self._load_context()
        
        # Command completion
        self.commands = [
            '/help', '/models', '/switch', '/tools', '/clear', '/history', '/context', 
            '/image', '/debug', '/analyze', '/exit', '/quit', '/edit-context', '/add-tool', 
            '/plan', '/theme', '/save-session', '/load-session', '/status', '/config'
        ]
    
    def _load_config(self):
        """Load configuration"""
        config = configparser.ConfigParser()
        config_file = "config.ini"
        
        if os.path.exists(config_file):
            config.read(config_file)
        else:
            # Create default config
            config['models'] = {
                'default': 'http://localhost:11434/v1/chat/completions',
                'ollama': 'http://localhost:11434/v1/chat/completions',
                'lmstudio': 'http://localhost:1234/v1/chat/completions'
            }
            config['settings'] = {
                'temperature': '0.7',
                'max_tokens': '2048',
                'timeout': '30'
            }
            
            with open(config_file, 'w') as f:
                config.write(f)
        
        return config
    
    def _load_context(self):
        """Load aicode.md context file"""
        context_file = "aicode.md"
        if os.path.exists(context_file):
            try:
                with open(context_file, 'r') as f:
                    content = f.read()
                    self.context = content.split('\n')
                console.print(f"[green]✓ Loaded context from {context_file}[/green]")
            except Exception as e:
                console.print(f"[yellow]Warning: Could not load context: {e}[/yellow]")
    
    def run(self):
        """Start the interactive shell"""
        console.print("╭──────────────────────────────────────────────────────────────╮")
        console.print("│ AiCode - Compact CLI Coding Assistant                       │")
        console.print("╰──────────────────────────────────────────────────────────────╯")
        
        if self.context:
            console.print(f"✓ Loaded context ({len(self.context)} lines)")
        
        console.print("Type '/help' for commands or start coding!")
        console.print(f"Model: {self.current_model} | Theme: {self.theme}")
        
        # Set up command completion
        completer = WordCompleter(self.commands)
        history = InMemoryHistory()
        
        while True:
            try:
                user_input = toolkit_prompt(
                    "aicode> ",
                    completer=completer,
                    history=history
                ).strip()
                
                if not user_input:
                    continue
                
                if user_input.startswith('/'):
                    if not self._handle_command(user_input):
                        break
                else:
                    self._process_conversation(user_input)
                    
            except (EOFError, KeyboardInterrupt):
                console.print("\n[yellow]Goodbye![/yellow]")
                break
    
    def _handle_command(self, command: str) -> bool:
        """Handle shell commands. Returns False to exit."""
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd in ['/exit', '/quit']:
            return False
        elif cmd == '/help':
            self._show_help()
        elif cmd == '/models':
            self._list_models()
        elif cmd == '/switch':
            if len(parts) > 1:
                self._switch_model(parts[1])
            else:
                model = Prompt.ask("Enter model endpoint or name")
                self._switch_model(model)
        elif cmd == '/tools':
            self._show_tools()
        elif cmd == '/clear':
            self.conversation_history = []
            console.print("[green]Conversation history cleared[/green]")
        elif cmd == '/history':
            self._show_history()
        elif cmd == '/context':
            self._show_context()
        elif cmd == '/debug':
            self._debug_mode()
        elif cmd == '/analyze':
            if len(parts) > 1:
                self._analyze_file(parts[1])
            else:
                file_path = Prompt.ask("Enter file path to analyze")
                self._analyze_file(file_path)
        elif cmd == '/edit-context':
            self._edit_context()
        elif cmd == '/add-tool':
            self._add_custom_tool()
        elif cmd == '/plan':
            if len(parts) > 1:
                self._create_plan(' '.join(parts[1:]))
            else:
                task = Prompt.ask("Enter task to plan")
                self._create_plan(task)
        elif cmd == '/theme':
            if len(parts) > 1:
                self._change_theme(parts[1])
            else:
                self._show_themes()
        elif cmd == '/save-session':
            name = parts[1] if len(parts) > 1 else None
            if name:
                self._save_session(name)
            else:
                self._save_session()
        elif cmd == '/load-session':
            if len(parts) > 1:
                self._load_session(parts[1])
            else:
                self._list_sessions()
        elif cmd == '/status':
            self._show_status()
        elif cmd == '/config':
            self._show_config()
        else:
            console.print(f"[red]Unknown command: {cmd}[/red]")
            console.print("Type '/help' for available commands")
        
        return True
    
    def _process_conversation(self, user_input: str):
        """Process user input and generate response"""
        # Check for tool calls
        if "TOOL:" in user_input.upper():
            self._execute_tool_request(user_input)
            return
        
        # Prepare messages for model
        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": user_input}
        ]
        
        # Add recent context
        if self.conversation_history:
            recent = self.conversation_history[-3:]
            for exchange in recent:
                messages.insert(-1, {"role": "user", "content": exchange['user']})
                messages.insert(-1, {"role": "assistant", "content": exchange['assistant']})
        
        # Send to model
        response = self._send_to_model(messages)
        
        if response:
            self._display_response(response)
            
            # Store in history
            self.conversation_history.append({
                'user': user_input,
                'assistant': response,
                'timestamp': datetime.now().isoformat()
            })
        else:
            console.print("[red]Error: Could not get response from model[/red]")
    
    def _get_system_prompt(self) -> str:
        """Get optimized system prompt"""
        base_prompt = """You are AiCode, a helpful coding assistant optimized for small local models. 
Be concise, practical, and focus on actionable solutions. 

Available tools: read_file, write_file, execute_command, analyze_code

When user asks for file operations or code analysis, suggest using tools like:
TOOL: read_file path=filename.py
TOOL: write_file path=filename.py content="code here"
TOOL: execute_command command="python script.py"
TOOL: analyze_code code="code to analyze" language="python"

Keep responses under 200 words unless explaining complex concepts."""
        
        if self.context:
            context_text = '\n'.join(self.context[:10])  # First 10 lines
            base_prompt += f"\n\nProject context:\n{context_text}"
        
        return base_prompt
    
    def _send_to_model(self, messages: List[Dict]) -> Optional[str]:
        """Send request to model endpoint"""
        endpoint = self.config['models'].get(self.current_model, self.config['models']['default'])
        
        payload = {
            "model": "gpt-3.5-turbo",  # Most local servers accept this
            "messages": messages,
            "temperature": float(self.config['settings'].get('temperature', '0.7')),
            "max_tokens": int(self.config['settings'].get('max_tokens', '2048'))
        }
        
        try:
            timeout = int(self.config['settings'].get('timeout', '30'))
            response = requests.post(endpoint, json=payload, timeout=timeout)
            
            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and data['choices']:
                    return data['choices'][0]['message']['content']
            else:
                console.print(f"[red]Model error: HTTP {response.status_code}[/red]")
                
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Connection error: {e}[/red]")
            console.print("[yellow]Check if your local model server is running[/yellow]")
        
        return None
    
    def _execute_tool_request(self, user_input: str):
        """Execute tool requests"""
        tool_pattern = r'TOOL:\s*(\w+)\s*([^\n]*)'
        matches = re.findall(tool_pattern, user_input, re.IGNORECASE)
        
        for tool_name, args_str in matches:
            result = self._execute_tool(tool_name, args_str)
            console.print(f"[cyan]Tool result ({tool_name}):[/cyan]")
            console.print(result)
    
    def _execute_tool(self, tool_name: str, args_str: str) -> str:
        """Execute a specific tool"""
        # Parse arguments
        args = {}
        if args_str:
            for arg in args_str.split():
                if '=' in arg:
                    key, value = arg.split('=', 1)
                    args[key] = value.strip('"\'')
        
        try:
            if tool_name == 'read_file':
                path = args.get('path', '')
                if not path:
                    return "Error: path parameter required"
                with open(path, 'r') as f:
                    return f.read()
            
            elif tool_name == 'write_file':
                path = args.get('path', '')
                content = args.get('content', '')
                if not path:
                    return "Error: path parameter required"
                with open(path, 'w') as f:
                    f.write(content)
                return f"File written: {path}"
            
            elif tool_name == 'execute_command':
                command = args.get('command', '')
                if not command:
                    return "Error: command parameter required"
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
                return f"Exit code: {result.returncode}\nOutput: {result.stdout}\nError: {result.stderr}"
            
            elif tool_name == 'analyze_code':
                code = args.get('code', '')
                if not code:
                    return "Error: code parameter required"
                return self._analyze_code_content(code)
            
            elif tool_name == 'list_files':
                path = args.get('path', '.')
                files = os.listdir(path)
                return '\n'.join(files)
            
            else:
                return f"Unknown tool: {tool_name}"
                
        except Exception as e:
            return f"Tool error: {str(e)}"
    
    def _analyze_code_content(self, code: str) -> str:
        """Analyze code content"""
        try:
            tree = ast.parse(code)
            
            functions = []
            classes = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    imports.append(f"from {node.module}")
            
            analysis = []
            analysis.append(f"Lines of code: {len(code.split())}")
            if functions:
                analysis.append(f"Functions: {', '.join(functions)}")
            if classes:
                analysis.append(f"Classes: {', '.join(classes)}")
            if imports:
                analysis.append(f"Imports: {', '.join(imports[:5])}")
            
            return '\n'.join(analysis)
            
        except SyntaxError as e:
            return f"Syntax Error: {e}"
        except Exception as e:
            return f"Analysis Error: {e}"
    
    def _show_help(self):
        """Show help information"""
        help_table = Table(title="AiCode Commands")
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="white")
        
        commands = [
            ("/help", "Show this help message"),
            ("/models", "List available models"),
            ("/switch <model>", "Switch to a different model"),
            ("/tools", "Show available tools"),
            ("/clear", "Clear conversation history"),
            ("/history", "Show conversation history"),
            ("/context", "Show current context"),
            ("/debug", "Enter debug mode"),
            ("/analyze <file>", "Analyze a code file"),
            ("/edit-context", "Edit aicode.md context file"),
            ("/add-tool", "Add custom tool"),
            ("/plan <task>", "Create project plan"),
            ("/theme [name]", "Change/show themes"),
            ("/save-session [name]", "Save current session"),
            ("/load-session [name]", "Load saved session"),
            ("/status", "Show system status"),
            ("/config", "Show configuration"),
            ("/exit, /quit", "Exit AiCode")
        ]
        
        for cmd, desc in commands:
            help_table.add_row(cmd, desc)
        
        console.print(help_table)
    
    def _list_models(self):
        """List available models"""
        models_table = Table(title="Available Models")
        models_table.add_column("Name", style="cyan")
        models_table.add_column("Endpoint", style="white")
        models_table.add_column("Status", style="green")
        
        for name, endpoint in self.config['models'].items():
            status = self._test_model_connection(endpoint)
            status_text = "✓ Connected" if status else "✗ Disconnected"
            models_table.add_row(name, endpoint, status_text)
        
        console.print(models_table)
    
    def _test_model_connection(self, endpoint: str) -> bool:
        """Test connection to model endpoint"""
        try:
            test_payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 10
            }
            response = requests.post(endpoint, json=test_payload, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _switch_model(self, model: str):
        """Switch to different model"""
        if model in self.config['models']:
            self.current_model = model
            console.print(f"[green]Switched to model: {model}[/green]")
        else:
            # Treat as custom endpoint
            self.config['models'][model] = model
            self.current_model = model
            console.print(f"[green]Added and switched to custom endpoint: {model}[/green]")
    
    def _show_tools(self):
        """Show available tools"""
        tools = [
            ("read_file", "Read file content", "path=filename"),
            ("write_file", "Write file content", "path=filename content=\"text\""),
            ("execute_command", "Run shell command", "command=\"python script.py\""),
            ("analyze_code", "Analyze code structure", "code=\"def hello(): pass\""),
            ("list_files", "List directory contents", "path=. (optional)")
        ]
        
        tools_table = Table(title="Available Tools")
        tools_table.add_column("Tool", style="cyan")
        tools_table.add_column("Description", style="white")
        tools_table.add_column("Usage", style="yellow")
        
        for tool, desc, usage in tools:
            tools_table.add_row(tool, desc, f"TOOL: {tool} {usage}")
        
        console.print(tools_table)
    
    def _show_history(self):
        """Show conversation history"""
        if not self.conversation_history:
            console.print("[yellow]No conversation history[/yellow]")
            return
        
        for i, exchange in enumerate(self.conversation_history[-5:], 1):
            console.print(f"\n[bold cyan]Exchange {i}:[/bold cyan]")
            console.print(f"[green]User:[/green] {exchange['user']}")
            console.print(f"[blue]Assistant:[/blue] {exchange['assistant'][:200]}{'...' if len(exchange['assistant']) > 200 else ''}")
    
    def _show_context(self):
        """Show current context"""
        if not self.context:
            console.print("[yellow]No context available[/yellow]")
            return
        
        console.print(f"[cyan]Context ({len(self.context)} lines):[/cyan]")
        for i, line in enumerate(self.context[:10], 1):
            console.print(f"{i:2d}: {line}")
        
        if len(self.context) > 10:
            console.print(f"... and {len(self.context) - 10} more lines")
    
    def _debug_mode(self):
        """Enhanced debug mode"""
        console.print("[bold cyan]🐛 Debug Mode[/bold cyan]")
        console.print("Commands: analyze <code>, trace <file>, errors, help, quit")
        
        while True:
            try:
                debug_cmd = input("(debug) ").strip()
                
                if debug_cmd in ['quit', 'q', 'exit']:
                    break
                elif debug_cmd.startswith('analyze'):
                    code = debug_cmd[7:].strip()
                    if code:
                        result = self._analyze_code_content(code)
                        console.print(result)
                    else:
                        console.print("[red]Usage: analyze <code>[/red]")
                elif debug_cmd.startswith('trace'):
                    file_path = debug_cmd[5:].strip()
                    if file_path and os.path.exists(file_path):
                        with open(file_path, 'r') as f:
                            content = f.read()
                        result = self._analyze_code_content(content)
                        console.print(f"[cyan]Analysis of {file_path}:[/cyan]")
                        console.print(result)
                    else:
                        console.print("[red]File not found[/red]")
                elif debug_cmd == 'errors':
                    if self.debug_history:
                        console.print("[cyan]Recent Errors:[/cyan]")
                        for error in self.debug_history[-5:]:
                            console.print(f"• {error}")
                    else:
                        console.print("[green]No errors recorded[/green]")
                elif debug_cmd == 'help':
                    console.print("""
[bold cyan]Debug Commands:[/bold cyan]
  analyze <code>  - Analyze code for syntax and structure
  trace <file>    - Analyze a Python file
  errors          - Show recent error history
  help            - Show this help
  quit            - Exit debug mode
""")
                else:
                    console.print(f"[red]Unknown debug command: {debug_cmd}[/red]")
                    
            except (EOFError, KeyboardInterrupt):
                break
        
        console.print("[yellow]Exited debug mode[/yellow]")
    
    def _analyze_file(self, file_path: str):
        """Analyze a code file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Display file with syntax highlighting
            syntax = Syntax(content, "python", theme="monokai", line_numbers=True)
            console.print(Panel(syntax, title=f"File: {file_path}"))
            
            # Analyze content
            analysis = self._analyze_code_content(content)
            console.print(f"[cyan]Analysis:[/cyan]")
            console.print(analysis)
            
        except Exception as e:
            console.print(f"[red]Error analyzing file: {e}[/red]")
    
    def _edit_context(self):
        """Edit aicode.md context file"""
        context_file = "aicode.md"
        
        if not os.path.exists(context_file):
            console.print("[yellow]Creating new aicode.md file[/yellow]")
            with open(context_file, 'w') as f:
                f.write("# AiCode Context\n\nAdd your project context here...\n")
        
        console.print(f"[cyan]Edit {context_file} in your preferred editor, then press Enter[/cyan]")
        input("Press Enter when done editing...")
        
        # Reload context
        self._load_context()
    
    def _add_custom_tool(self):
        """Add custom tool"""
        name = Prompt.ask("Tool name")
        command = Prompt.ask("Shell command")
        
        if name and command:
            # Save to custom tools file
            tools_file = "custom_tools.json"
            tools_data = {}
            
            if os.path.exists(tools_file):
                with open(tools_file, 'r') as f:
                    tools_data = json.load(f)
            
            tools_data[name] = command
            
            with open(tools_file, 'w') as f:
                json.dump(tools_data, f, indent=2)
            
            console.print(f"[green]Added custom tool '{name}'[/green]")
            console.print(f"[cyan]Usage: TOOL: {name}[/cyan]")
    
    def _create_plan(self, task: str):
        """Create project plan"""
        plan_id = f"plan_{len(self.plans) + 1}"
        
        phases = [
            {"name": "Planning", "tasks": ["Analyze requirements", "Design structure"], "hours": 2},
            {"name": "Implementation", "tasks": ["Core functionality", "Error handling"], "hours": 6},
            {"name": "Testing", "tasks": ["Unit tests", "Integration tests"], "hours": 2}
        ]
        
        plan = {
            'task': task,
            'phases': phases,
            'total_hours': sum(p['hours'] for p in phases),
            'created': datetime.now().isoformat()
        }
        
        self.plans[plan_id] = plan
        
        # Display plan
        console.print(f"[bold cyan]Plan Created: {task}[/bold cyan]")
        table = Table(title="Project Phases")
        table.add_column("Phase", style="cyan")
        table.add_column("Tasks", style="white")
        table.add_column("Hours", style="yellow")
        
        for phase in phases:
            table.add_row(phase['name'], ', '.join(phase['tasks']), str(phase['hours']))
        
        console.print(table)
        console.print(f"[bold]Total estimated time: {plan['total_hours']} hours[/bold]")
    
    def _change_theme(self, theme_name: str):
        """Change color theme"""
        if theme_name in self.themes:
            self.theme = theme_name
            theme = self.themes[theme_name]
            console.print(f"[{theme['success']}]✓ Changed to {theme_name} theme[/{theme['success']}]")
        else:
            console.print(f"[red]Theme '{theme_name}' not found[/red]")
    
    def _show_themes(self):
        """Show available themes"""
        console.print("[bold cyan]Available Themes[/bold cyan]")
        
        for name, colors in self.themes.items():
            is_current = " (current)" if name == self.theme else ""
            console.print(f"[{colors['primary']}]• {name}{is_current}[/{colors['primary']}]")
    
    def _save_session(self, name: Optional[str] = None):
        """Save current session"""
        if not name:
            name = f"session_{datetime.now().strftime('%Y%m%d_%H%M')}"
        
        session_data = {
            'conversation_history': self.conversation_history,
            'context': self.context,
            'current_model': self.current_model,
            'theme': self.theme,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            sessions_file = "sessions.json"
            all_sessions = {}
            
            if os.path.exists(sessions_file):
                with open(sessions_file, 'r') as f:
                    all_sessions = json.load(f)
            
            all_sessions[name] = session_data
            
            with open(sessions_file, 'w') as f:
                json.dump(all_sessions, f, indent=2)
            
            console.print(f"[green]Session saved as '{name}'[/green]")
        except Exception as e:
            console.print(f"[red]Error saving session: {e}[/red]")
    
    def _load_session(self, name: str):
        """Load saved session"""
        try:
            sessions_file = "sessions.json"
            
            if os.path.exists(sessions_file):
                with open(sessions_file, 'r') as f:
                    all_sessions = json.load(f)
                
                if name in all_sessions:
                    session_data = all_sessions[name]
                    self.conversation_history = session_data.get('conversation_history', [])
                    self.context = session_data.get('context', [])
                    self.current_model = session_data.get('current_model', 'default')
                    self.theme = session_data.get('theme', 'default')
                    
                    console.print(f"[green]Session '{name}' loaded[/green]")
                else:
                    console.print(f"[red]Session '{name}' not found[/red]")
            else:
                console.print("[yellow]No saved sessions found[/yellow]")
        except Exception as e:
            console.print(f"[red]Error loading session: {e}[/red]")
    
    def _list_sessions(self):
        """List saved sessions"""
        try:
            sessions_file = "sessions.json"
            
            if os.path.exists(sessions_file):
                with open(sessions_file, 'r') as f:
                    all_sessions = json.load(f)
                
                if all_sessions:
                    console.print("[cyan]Saved Sessions:[/cyan]")
                    for name, data in all_sessions.items():
                        timestamp = data.get('timestamp', 'unknown')
                        console.print(f"  • {name} ({timestamp})")
                else:
                    console.print("[yellow]No saved sessions[/yellow]")
            else:
                console.print("[yellow]No saved sessions found[/yellow]")
        except Exception as e:
            console.print(f"[red]Error listing sessions: {e}[/red]")
    
    def _show_status(self):
        """Show system status"""
        console.print("[bold cyan]AiCode Status[/bold cyan]")
        
        # Model status
        console.print(f"[green]Model:[/green] {self.current_model}")
        endpoint = self.config['models'].get(self.current_model, '')
        is_connected = self._test_model_connection(endpoint)
        status = "Connected" if is_connected else "Disconnected"
        color = "green" if is_connected else "red"
        console.print(f"[green]Connection:[/green] [{color}]{status}[/{color}]")
        
        # Other status
        console.print(f"[green]Theme:[/green] {self.theme}")
        context_status = f"{len(self.context)} lines loaded" if self.context else "No context loaded"
        console.print(f"[green]Context:[/green] {context_status}")
        console.print(f"[green]History:[/green] {len(self.conversation_history)} exchanges")
    
    def _show_config(self):
        """Show current configuration"""
        console.print("[bold cyan]Configuration[/bold cyan]")
        
        for section_name in self.config.sections():
            console.print(f"\n[yellow]{section_name.upper()}:[/yellow]")
            for key, value in self.config[section_name].items():
                # Hide sensitive values
                if any(secret in key.lower() for secret in ['key', 'token', 'password']):
                    value = "***"
                console.print(f"  {key}: {value}")
    
    def _display_response(self, response: str):
        """Display model response with formatting"""
        if '```' in response:
            console.print(Markdown(response))
        else:
            console.print(Panel(response, border_style="blue", title="Response"))

def main():
    """Main entry point"""
    try:
        aicode = CompactAiCode()
        aicode.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()