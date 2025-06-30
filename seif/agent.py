# seifcli/seif/agent.py - Enhanced Version

import pkgutil
import importlib
import re
import json
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from . import skills
from .planner import Planner
from .browser import Browser

console = Console()

class Agent:
    def __init__(self, config_path: Optional[str] = None, model: Optional[str] = None):
        self.model = model
        self.browser = None
        self.skills = self._load_skills()
        self.execution_log = []
        self.config = self._load_config(config_path)
        
        self.planner = Planner(model=self.model)
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file or use defaults."""
        default_config = {
            "browser": {
                "headless": False,
                "window_size": "1920,1080",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "timeout": 10
            },
            "security": {
                "require_confirmation": True,
                "safe_domains": ["google.com", "github.com", "stackoverflow.com"],
                "blocked_commands": []
            },
            "logging": {
                "save_screenshots_on_error": True,
                "log_file": "agent_execution.log"
            }
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    for key, value in user_config.items():
                        if isinstance(value, dict):
                            default_config[key].update(value)
                        else:
                            default_config[key] = value
            except Exception as e:
                console.print(f"[yellow]Warning: Could not load config from {config_path}: {e}[/yellow]")
        
        return default_config

    def _initialize_browser(self):
        """Initializes the browser if it hasn't been already."""
        if self.browser is None:
            self.browser = Browser(config=self.config.get("browser", {}))

    def _load_skills(self) -> Dict:
        """Dynamically loads all skills from the 'skills' directory."""
        discovered_skills = {}
        skills_table = Table(title="Loaded Skills")
        skills_table.add_column("Command", style="bold blue")
        skills_table.add_column("Function", style="green")
        skills_table.add_column("Module", style="dim")
        
        for _, name, _ in pkgutil.iter_modules(skills.__path__, skills.__name__ + "."):
            try:
                module = importlib.import_module(name)
                if hasattr(module, "SKILLS"):
                    for command, func in module.SKILLS.items():
                        discovered_skills[command] = func
                        skills_table.add_row(command, func.__name__, name.split('.')[-1])
            except Exception as e:
                console.print(f"[red]Failed to load skill from {name}: {e}[/red]")
        
        console.print(skills_table)
        return discovered_skills

    def _parse_command(self, command_str: str) -> Tuple[Optional[str], List[str]]:
        """Enhanced command parsing with better error handling."""
        try:
            pattern = r'(\w+)(?:\s+"([^"]*)")*(?:\s+(\S+))*'
            match = re.match(pattern, command_str.strip())
            
            if not match:
                parts = re.findall(r'(\w+)|"(.*?)"', command_str)
                command = None
                args = []
                
                for part in parts:
                    if part[0] and not command:
                        command = part[0]
                    elif part[1]:
                        args.append(part[1])
                    elif part[0] and command:
                        args.append(part[0])
                        
                return command, args
            
            command = match.group(1)
            args = [g for g in match.groups()[1:] if g is not None]
            return command, args
            
        except Exception as e:
            console.print(f"[red]Error parsing command '{command_str}': {e}[/red]")
            return None, []

    def _log_execution(self, step: str, command: str, args: List[str], 
                      success: bool, error: Optional[str] = None):
        """Log execution details for debugging and analysis."""
        log_entry = {
            "timestamp": time.time(),
            "step": step,
            "command": command,
            "args": args,
            "success": success,
            "error": error
        }
        self.execution_log.append(log_entry)
        
        if self.config.get("logging", {}).get("log_file"):
            try:
                log_file = Path(self.config["logging"]["log_file"])
                with open(log_file, 'a') as f:
                    f.write(f"{json.dumps(log_entry)}\n")
            except Exception:
                pass  

    def _is_safe_domain(self, url: str) -> bool:
        """Check if URL is in the safe domains list."""
        safe_domains = self.config.get("security", {}).get("safe_domains", [])
        return any(domain in url for domain in safe_domains)

    def _requires_confirmation(self, command: str, args: List[str]) -> bool:
        """Determine if a command requires user confirmation."""
        if not self.config.get("security", {}).get("require_confirmation", True):
            return False
            
        if command in ["CLICK", "TYPE"]:
            return True
            
        if command == "GOTO" and args:
            return not self._is_safe_domain(args[0])
            
        return False

    def execute_task(self, prompt: str, interactive_mode: bool = False, 
                    dry_run: bool = False):
        """Enhanced task execution with better error handling and logging."""
        self._initialize_browser()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            plan_task = progress.add_task("Creating plan...", total=None)
            plan = self.planner.create_plan(prompt)
            progress.remove_task(plan_task)
        
        if not plan:
            console.print("[bold red]Could not create a plan. Aborting.[/bold red]")
            return False

        console.print(f"[bold green]Plan created with {len(plan)} steps[/bold green]")
        
        if dry_run:
            console.print("[yellow]DRY RUN MODE - No actions will be executed[/yellow]")
            for i, step in enumerate(plan, 1):
                console.print(f"  {i}. {step}")
            return True

        success = True
        i = 0
        
        while i < len(plan):
            step = plan[i]
            console.print(f"\n[yellow]Step {i+1}/{len(plan)}: {step}[/yellow]")
            
            command, args = self._parse_command(step)
            
            if not command:
                console.print(f"[red]Could not parse command: {step}[/red]")
                self._log_execution(step, "", [], False, "Parse error")
                break
            
            if self._requires_confirmation(command, args):
                if not Confirm.ask(f"⚠️ Proceed with [bold cyan]{command}[/bold cyan] {' '.join(args)}?", default=True):
                    console.print("[bold red]Aborted by user.[/bold red]")
                    self._log_execution(step, command, args, False, "User abort")
                    success = False
                    break
            
            error = self._execute_command(command, args, step)
            
            if error:
                console.print(f"[bold red]Error: {error}[/bold red]")
                self._log_execution(step, command, args, False, error)
                
                if self.config.get("logging", {}).get("save_screenshots_on_error"):
                    error_screenshot = f"error_step_{i+1}_{int(time.time())}.png"
                    if self.browser:
                        self.browser.screenshot(error_screenshot)
                        console.print(f"[yellow]Error screenshot saved: {error_screenshot}[/yellow]")
                
                action = Prompt.ask(
                    "[yellow]What would you like to do?[/yellow]", 
                    choices=["retry", "skip", "abort"], 
                    default="skip"
                )
                
                if action == "retry":
                    continue
                elif action == "skip":
                    i += 1
                    continue
                else:
                    console.print("[bold red]Aborted by user.[/bold red]")
                    success = False
                    break
            else:
                self._log_execution(step, command, args, True)
                
            i += 1
        
        self._display_execution_summary()
        
        if not interactive_mode:
            self.close_browser()
            
        return success

    def _execute_command(self, command: str, args: List[str], step: str) -> Optional[str]:
        """Execute a single command and return error message if any."""
        try:
            if command == "GOTO":
                return self.browser.goto(args[0]) if args else "No URL provided"
            elif command == "TYPE":
                if len(args) < 2:
                    return "TYPE requires selector and text arguments"
                return self.browser.type(args[0], args[1])
            elif command == "CLICK":
                return self.browser.click(args[0]) if args else "No selector provided"
            elif command == "SCROLL":
                return self.browser.scroll(args[0]) if args else "No direction provided"
            elif command in self.skills:
                result = self.skills[command](self.browser, *args)
                console.print(f"[green]Skill {command} executed: {result}[/green]")
                return None
            elif command == "DONE":
                console.print("[bold green]Task completed successfully![/bold green]")
                return None
            else:
                return f"Unknown command: {command}"
                
        except Exception as e:
            return f"Unexpected error executing '{step}': {e}"

    def _display_execution_summary(self):
        """Display a summary of the execution."""
        if not self.execution_log:
            return
            
        successful = sum(1 for entry in self.execution_log if entry["success"])
        failed = len(self.execution_log) - successful
        
        summary_table = Table(title="Execution Summary")
        summary_table.add_column("Metric", style="bold")
        summary_table.add_column("Value", style="green")
        
        summary_table.add_row("Total Steps", str(len(self.execution_log)))
        summary_table.add_row("Successful", str(successful))
        summary_table.add_row("Failed", str(failed))
        summary_table.add_row("Success Rate", f"{(successful/len(self.execution_log)*100):.1f}%")
        
        console.print(summary_table)

    def get_execution_log(self) -> List[Dict]:
        """Return the execution log for analysis."""
        return self.execution_log.copy()

    def close_browser(self):
        """Close the browser and cleanup."""
        if self.browser:
            self.browser.close()
            self.browser = None