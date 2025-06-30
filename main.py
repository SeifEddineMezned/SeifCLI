#!/usr/bin/env python3
"""
SeifCLI - Your smart terminal assistant
Main entry point for the CLI application
"""

import typer
from typing import Optional
from pathlib import Path
import sys
import os


sys.path.insert(0, str(Path(__file__).parent))

from seif.agent import Agent
from seif.utils import display_startup_ui  
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
import time

app = typer.Typer(
    name="seif",
    help="🤖 SeifCLI - Your smart terminal assistant powered by local LLMs",
    add_completion=False,
    rich_markup_mode="rich"
)

console = Console()

@app.command("run")
def run_task(
    prompt: str = typer.Argument(..., help="Natural language task to execute"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Keep browser open after task completion"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed execution logs")
):
    """
    🚀 Execute a natural language task using AI and browser automation
    """
    console.print(f"\n[bold green]🎯 Task:[/bold green] {prompt}")
    console.print(f"[bold blue]🔧 Interactive Mode:[/bold blue] {'Enabled' if interactive else 'Disabled'}")
    
    if not Confirm.ask("🚀 Ready to execute this task?", default=True):
        console.print("[bold red]❌ Task cancelled by user.[/bold red]")
        return
    
    try:
        agent = Agent()
        agent.execute_task(prompt, interactive_mode=interactive)
        
        if interactive:
            console.print("\n[bold yellow]🔄 Interactive mode enabled - browser will remain open.[/bold yellow]")
            console.print("[dim]Press Ctrl+C to close the browser and exit.[/dim]")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                console.print("\n[bold blue]👋 Closing browser and exiting...[/bold blue]")
                agent.close_browser()
                
    except KeyboardInterrupt:
        console.print("\n[bold red]❌ Task interrupted by user.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]❌ Error executing task: {e}[/bold red]")

@app.command("chat")
def chat_mode(
    model: str = typer.Option(None, help="Local LLM model to use (overrides config)"),
    provider: str = typer.Option(None, help="LLM provider to use (ollama, openai, llama_cpp)"),
    save_history: bool = typer.Option(False, "--save", "-s", help="Save chat history on exit"),
    load_history: str = typer.Option(None, "--load", "-l", help="Load chat history from file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed logs")
):
    """
    💬 Start interactive chat mode with your AI assistant
    """
    console.print(Panel(
        "[bold cyan]Welcome to SeifCLI Chat Mode! 💬[/bold cyan]\n\n"
        "You can now chat with your AI assistant and execute browser tasks.\n"
        "Type 'help' for commands, 'exit' to quit, or just chat naturally!\n\n"
        "🤖 Your assistant can control browsers, take screenshots, and more!",
        title="🚀 Chat Mode",
        border_style="green"
    ))
    
    
    agent = Agent(model=model)
    
    
    from seif.chat_manager import ChatManager
    chat_manager = ChatManager(model=model)
    
    
    if load_history:
        from seif.memory import Memory
        memory = Memory()
        memory.load(load_history)
    
    try:
        while True:
            try:
                user_input = Prompt.ask("\n[bold blue]You[/bold blue]", default="")
                
                if not user_input.strip():
                    continue
                
                # Process the user input
                result = chat_manager.process_input(user_input)
                
                # Handle the result based on action type
                if result["action"] == "exit":
                    console.print("[bold yellow]👋 Goodbye![/bold yellow]")
                    
                    # Save chat history if requested
                    if save_history:
                        chat_manager.memory.save()
                        
                    break
                    
                elif result["action"] == "help":
                    show_chat_help()
                    continue
                    
                elif result["action"] == "clear":
                    console.clear()
                    display_startup_ui()
                    continue
                    
                elif result["action"] == "message":
                    console.print(f"[bold green]🤖 Assistant:[/bold green]")
                    console.print(result["content"])
                    continue
                    
                elif result["action"] == "task":
                    task = result["content"]
                    console.print(f"[bold green]🎯 Executing task:[/bold green] {task}")
                    agent.execute_task(task, interactive_mode=True)
                    continue
                    
                elif result["action"] == "chat":
                    # Generate and display response
                    response = chat_manager.generate_response(user_input)
                    chat_manager.display_response(response)
                
            except KeyboardInterrupt:
                console.print("\n[bold yellow]Use 'exit' to quit properly.[/bold yellow]")
                continue
                
    except Exception as e:
        console.print(f"[bold red]❌ Chat error: {e}[/bold red]")
    finally:
        console.print("[bold blue]🔧 Cleaning up browser session...[/bold blue]")
        agent.close_browser()

def show_chat_help():
    """Display help information for chat mode"""
    help_text = """
# 🚀 SeifCLI Chat Mode Help

## Available Commands:
- **help** - Show this help message
- **exit/quit/bye** - Exit chat mode
- **clear** - Clear the screen
- **clear history** - Clear conversation history
- **save history [filename]** - Save conversation history to a file
- **load history <filename>** - Load conversation history from a file
- **task: <command>** - Execute a browser task

## Examples:
- `task: search for Python tutorials on YouTube`
- `task: go to GitHub and search for machine learning projects`
- `task: navigate to ProductHunt and take a screenshot`
- `task: open Twitter and search for trending topics`

## Tips:
- The browser session stays open between tasks in chat mode
- You can chain multiple tasks together
- Type naturally - the AI will understand your intent
- Use Ctrl+C to interrupt a running task
- Use the --save flag when starting chat to automatically save history on exit
    """
    console.print(Markdown(help_text))

@app.command("version")
def show_version():
    """📋 Show SeifCLI version information"""
    version_info = """
# 🤖 SeifCLI v0.2.0

**Your smart terminal assistant powered by local LLMs**

- 🧠 Multiple LLM backends (Ollama, OpenAI, llama.cpp)
- 🌐 Browser automation (Selenium)
- 💬 Chat with conversation memory
- 🎨 Rich terminal interface
- 🔧 Modular plugin system
- 🔒 Secure execution with confirmations
- ⚙️ Flexible configuration system

Built with ❤️ for developers who want AI assistance with or without API dependencies.
    """
    console.print(Markdown(version_info))

@app.command("setup")
def setup_environment(
    skip_dependencies: bool = typer.Option(False, "--skip-deps", help="Skip dependency check and installation")
):
    """🔧 Setup SeifCLI environment and configuration"""
    import json
    from pathlib import Path
    import shutil
    import importlib.util
    
    console.print(Panel(
        "[bold cyan]SeifCLI Environment Setup 🔧[/bold cyan]\n\n"
        "This wizard will help you set up SeifCLI with your preferences.",
        title="Setup Wizard",
        border_style="blue"
    ))
    
    # Check dependencies if not skipped
    if not skip_dependencies:
        console.print("\n[bold]Checking dependencies...[/bold]")
        
        # Check for Ollama
        with console.status("[bold blue]Checking for Ollama...[/bold blue]"):
            ollama_installed = shutil.which("ollama") is not None
            time.sleep(1)
        
        if ollama_installed:
            console.print("[green]✓[/green] Ollama is installed")
        else:
            console.print("[yellow]⚠[/yellow] Ollama not found. Please install from https://ollama.ai")
        
        # Check for Python packages
        required_packages = ["selenium", "rich", "typer", "requests"]
        missing_packages = []
        
        with console.status("[bold blue]Checking Python packages...[/bold blue]"):
            for package in required_packages:
                if importlib.util.find_spec(package) is None:
                    missing_packages.append(package)
            time.sleep(1)
        
        if not missing_packages:
            console.print("[green]✓[/green] All required Python packages are installed")
        else:
            console.print(f"[yellow]⚠[/yellow] Missing packages: {', '.join(missing_packages)}")
            console.print("[dim]Run: pip install -r requirements.txt[/dim]")
    
    # Configuration setup
    console.print("\n[bold]Setting up configuration...[/bold]")
    
    # Create config directory if it doesn't exist
    config_dir = Path.home() / ".seifcli"
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "config.json"
    
    # Check if config file already exists
    if config_file.exists() and not Confirm.ask("Configuration file already exists. Overwrite?", default=False):
        console.print("[yellow]⚠[/yellow] Setup aborted. Using existing configuration.")
        return
    
    # Get user preferences
    console.print("\n[bold]LLM Configuration:[/bold]")
    
    # LLM provider
    provider_options = ["ollama", "openai", "llama_cpp"]
    provider = Prompt.ask(
        "LLM provider", 
        choices=provider_options,
        default="ollama"
    )
    
    # Model selection
    default_models = {
        "ollama": "mistral",
        "openai": "gpt-3.5-turbo",
        "llama_cpp": "llama-2-13b-chat.Q4_K_M.gguf"
    }
    
    model = Prompt.ask("Model name", default=default_models[provider])
    
    # API key for OpenAI
    api_key = ""
    if provider == "openai":
        api_key = Prompt.ask("OpenAI API key", password=True)
    
    # Browser configuration
    console.print("\n[bold]Browser Configuration:[/bold]")
    headless = Confirm.ask("Run browser in headless mode?", default=False)
    
    # Security configuration
    console.print("\n[bold]Security Configuration:[/bold]")
    require_confirmation = Confirm.ask("Require confirmation for sensitive actions?", default=True)
    
    # Memory configuration
    console.print("\n[bold]Memory Configuration:[/bold]")
    auto_summarize = Confirm.ask("Enable automatic conversation summarization?", default=True)
    
    # Create configuration
    config = {
        "llm": {
            "provider": provider,
            "model": model,
            "temperature": 0.7,
            "max_tokens": 2000,
            "api_key": api_key
        },
        "browser": {
            "headless": headless,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "timeout": 30,
            "screenshot_dir": str(config_dir / "screenshots")
        },
        "security": {
            "safe_domains": [
                "google.com",
                "github.com",
                "stackoverflow.com",
                "wikipedia.org",
                "python.org"
            ],
            "require_confirmation": require_confirmation,
            "confirmation_actions": ["CLICK", "TYPE", "GOTO"]
        },
        "memory": {
            "storage_dir": str(config_dir / "memory"),
            "max_context_length": 4000,
            "auto_summarize": auto_summarize,
            "summarization_threshold": 20
        },
        "logging": {
            "enabled": True,
            "level": "INFO",
            "file": str(config_dir / "seifcli.log")
        }
    }
    
    # Save configuration
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    # Create directories
    (config_dir / "screenshots").mkdir(exist_ok=True)
    (config_dir / "memory").mkdir(exist_ok=True)
    
    console.print(f"\n[green]✓[/green] Configuration saved to {config_file}")
    console.print("\n[bold yellow]💡 Tip:[/bold yellow] Run `seif run 'test the setup'` to verify everything works!")
    console.print("[bold yellow]💡 Tip:[/bold yellow] Run `seif chat` to start chatting with your assistant!")


def main():
    """Main entry point for the CLI"""
    display_startup_ui()  
    app()

if __name__ == "__main__":
    main()
