# seifcli/seif/config.py

import os
import json
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt

console = Console()

class Config:
    """
    Configuration manager for SeifCLI.
    Handles loading, saving, and accessing configuration settings.
    """
    
    # Default configuration
    DEFAULT_CONFIG = {
        "llm": {
            "provider": "ollama",  # 'ollama', 'llama_cpp', or 'openai'
            "model": "mistral",    # Default model name
            "api_key": "",        # Only used for API-based providers
            "temperature": 0.7,    # Creativity level (0.0 to 1.0)
            "max_tokens": 1000     # Maximum response length
        },
        "browser": {
            "headless": False,     # Run browser in headless mode
            "stealth_mode": True,  # Use stealth mode to avoid detection
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
        },
        "security": {
            "confirm_actions": True,  # Ask for confirmation before sensitive actions
            "safe_browsing": True     # Enable safe browsing checks
        },
        "skills": {
            "custom_skills_path": ""  # Path to custom skills directory
        },
        "ui": {
            "color_theme": "default",  # Terminal color theme
            "verbose_logging": False    # Enable verbose logging
        }
    }
    
    def __init__(self):
        """
        Initialize the configuration manager.
        """
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()
        
    def _get_config_dir(self) -> Path:
        """
        Get the configuration directory path.
        Creates the directory if it doesn't exist.
        """
        if os.name == "nt":  
            config_dir = Path(os.environ.get("APPDATA")) / "SeifCLI"
        else:  
            config_dir = Path.home() / ".config" / "seifcli"
            
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
        
    def _load_config(self) -> dict:
        """
        Load configuration from file or create default if not exists.
        """
        if not self.config_file.exists():
            
            self._save_config(self.DEFAULT_CONFIG)
            console.print(f"[yellow]Created default configuration at {self.config_file}[/yellow]")
            return self.DEFAULT_CONFIG
            
        try:
            with open(self.config_file, "r") as f:
                config = json.load(f)
                
            
            merged_config = self.DEFAULT_CONFIG.copy()
            self._deep_update(merged_config, config)
            return merged_config
        except Exception as e:
            console.print(f"[bold red]Error loading config: {e}[/bold red]")
            console.print("[yellow]Using default configuration[/yellow]")
            return self.DEFAULT_CONFIG
            
    def _save_config(self, config: dict) -> None:
        """
        Save configuration to file.
        """
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            console.print(f"[bold red]Error saving config: {e}[/bold red]")
            
    def _deep_update(self, target: dict, source: dict) -> None:
        """
        Deep update a nested dictionary with another dictionary.
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
                
    def get(self, section: str, key: str, default=None):
        """
        Get a configuration value.
        
        Args:
            section: Configuration section (e.g., 'llm', 'browser')
            key: Configuration key within the section
            default: Default value if not found
            
        Returns:
            The configuration value or default
        """
        try:
            return self.config[section][key]
        except KeyError:
            return default
            
    def set(self, section: str, key: str, value) -> None:
        """
        Set a configuration value and save to file.
        
        Args:
            section: Configuration section (e.g., 'llm', 'browser')
            key: Configuration key within the section
            value: Value to set
        """
        if section not in self.config:
            self.config[section] = {}
            
        self.config[section][key] = value
        self._save_config(self.config)
        
    def get_all(self) -> dict:
        """
        Get the entire configuration dictionary.
        
        Returns:
            The complete configuration dictionary
        """
        return self.config
        
    def reset(self) -> None:
        """
        Reset configuration to defaults.
        """
        self.config = self.DEFAULT_CONFIG.copy()
        self._save_config(self.config)
        console.print("[green]Configuration reset to defaults.[/green]")
        
    def setup_wizard(self) -> None:
        """
        Interactive configuration wizard.
        """
        console.print("[bold cyan]SeifCLI Configuration Wizard[/bold cyan]")
        console.print("Configure your SeifCLI settings. Press Enter to keep default values.\n")
        
        
        console.print("[bold]LLM Settings:[/bold]")
        provider = Prompt.ask(
            "LLM Provider", 
            choices=["ollama", "llama_cpp", "openai"], 
            default=self.config["llm"]["provider"]
        )
        model = Prompt.ask("Model name", default=self.config["llm"]["model"])
        
        
        api_key = ""
        if provider == "openai":
            api_key = Prompt.ask("API Key", default=self.config["llm"]["api_key"], password=True)
            
        
        console.print("\n[bold]Browser Settings:[/bold]")
        headless = Prompt.ask(
            "Run browser in headless mode", 
            choices=["True", "False"], 
            default=str(self.config["browser"]["headless"])
        ) == "True"
        
        
        console.print("\n[bold]Security Settings:[/bold]")
        confirm_actions = Prompt.ask(
            "Confirm before sensitive actions", 
            choices=["True", "False"], 
            default=str(self.config["security"]["confirm_actions"])
        ) == "True"
        
        
        self.set("llm", "provider", provider)
        self.set("llm", "model", model)
        if provider == "openai":
            self.set("llm", "api_key", api_key)
        self.set("browser", "headless", headless)
        self.set("security", "confirm_actions", confirm_actions)
        
        console.print("\n[bold green]Configuration saved successfully![/bold green]")


config = Config()