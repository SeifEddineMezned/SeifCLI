import ollama
from rich.console import Console
from rich.status import Status
from rich.prompt import Prompt
import json
import os
from pathlib import Path
import time

from .config import config

console = Console()

class LLM:
    def __init__(self, model=None):
        """
        Initializes the LLM client.
        Defaults to the model specified in config or "mistral" if not configured.
        """
        
        self.model = model or config.get("llm", "model", "mistral")
        self.provider = config.get("llm", "provider", "ollama")
        self.temperature = config.get("llm", "temperature", 0.7)
        self.max_tokens = config.get("llm", "max_tokens", 1000)
        
 
        self.conversation_history = []
        
        
        self._initialize_client()
        
    def _initialize_client(self):
        """
        Initialize the appropriate LLM client based on the provider.
        """
        if self.provider == "ollama":
            self._initialize_ollama()
        elif self.provider == "llama_cpp":
            self._initialize_llama_cpp()
        elif self.provider == "openai":
            self._initialize_openai()
        else:
            console.print(f"[bold red]Unknown LLM provider: {self.provider}[/bold red]")
            console.print("[yellow]Falling back to Ollama...[/yellow]")
            self.provider = "ollama"
            self._initialize_ollama()
    
    def _initialize_ollama(self):
        """
        Initialize the Ollama client.
        """
        try:
            self.client = ollama.Client()
            self._check_model_availability()
        except Exception as e:
            console.print(f"[bold red]Error initializing Ollama client: {e}[/bold red]")
            console.print("[bold yellow]Please ensure Ollama is running and the model is available.[/bold yellow]")
            self.client = None
    
    def _initialize_llama_cpp(self):
        """
        Initialize the llama.cpp client.
        This is a placeholder for future implementation.
        """
        try:
           
            console.print("[yellow]llama.cpp support is not yet implemented.[/yellow]")
            console.print("[yellow]Falling back to Ollama...[/yellow]")
            self.provider = "ollama"
            self._initialize_ollama()
        except ImportError:
            console.print("[bold red]llama-cpp-python is not installed.[/bold red]")
            console.print("[yellow]Install with: pip install llama-cpp-python[/yellow]")
            console.print("[yellow]Falling back to Ollama...[/yellow]")
            self.provider = "ollama"
            self._initialize_ollama()
    
    def _initialize_openai(self):
        """
        Initialize the OpenAI client.
        This is a placeholder for future implementation.
        """
        try:
            
            api_key = config.get("llm", "api_key", "")
            if not api_key:
                console.print("[bold red]OpenAI API key not configured.[/bold red]")
                console.print("[yellow]Falling back to Ollama...[/yellow]")
                self.provider = "ollama"
                self._initialize_ollama()
                return
                
            
            console.print("[yellow]OpenAI support is not yet implemented.[/yellow]")
            console.print("[yellow]Falling back to Ollama...[/yellow]")
            self.provider = "ollama"
            self._initialize_ollama()
        except ImportError:
            console.print("[bold red]openai package is not installed.[/bold red]")
            console.print("[yellow]Install with: pip install openai[/yellow]")
            console.print("[yellow]Falling back to Ollama...[/yellow]")
            self.provider = "ollama"
            self._initialize_ollama()

    def _check_model_availability(self):
        """
        Checks if the specified model is available locally.
        """
        if not self.client or self.provider != "ollama":
            return
        try:
            models = self.client.list()["models"]
            if not any(m.get('name', '').startswith(self.model) for m in models):
                console.print(f"[bold yellow]Warning: Model '{self.model}' not found. Attempting to pull it...[/bold yellow]")
                self._pull_model()
        except Exception as e:
            console.print(f"[bold red]Could not verify model availability: {e}[/bold red]")

    def _pull_model(self):
        """
        Pulls the model from Ollama.
        """
        if self.provider != "ollama":
            return
            
        try:
            with console.status(f"[bold green]Pulling model '{self.model}'...[/bold green]", spinner="dots") as status:
                ollama.pull(self.model)
            console.print(f"[bold green]Model '{self.model}' pulled successfully.[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Failed to pull model '{self.model}': {e}[/bold red]")

    def generate(self, prompt: str, system_prompt: str = None, with_history: bool = False) -> str:
        """
        Generates a response from the LLM.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            with_history: Whether to include conversation history
            
        Returns:
            The generated response
        """
        if self.provider == "ollama":
            return self._generate_ollama(prompt, system_prompt, with_history)
        elif self.provider == "llama_cpp":
            return "llama.cpp support is not yet implemented."
        elif self.provider == "openai":
            return "OpenAI support is not yet implemented."
        else:
            return f"Unknown provider: {self.provider}"

    def _generate_ollama(self, prompt: str, system_prompt: str = None, with_history: bool = False) -> str:
        """
        Generates a response using Ollama.
        """
        if not self.client:
            return "Ollama client not initialized."
            
        messages = []
        
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        
        if with_history and self.conversation_history:
            messages.extend(self.conversation_history)
        
        
        messages.append({"role": "user", "content": prompt})

        try:
            with console.status("[bold green]Generating response...[/bold green]", spinner="dots") as status:
                response = self.client.chat(
                    model=self.model,
                    messages=messages,
                    options={
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens
                    }
                )
            
            content = response['message']['content']
            
            
            if with_history:
                self.conversation_history.append({"role": "user", "content": prompt})
                self.conversation_history.append({"role": "assistant", "content": content})
                
            return content
        except Exception as e:
            console.print(f"[bold red]Error during model generation: {e}[/bold red]")
            return "Error generating response."

    def add_to_history(self, role: str, content: str):
        """
        Manually add a message to the conversation history.
        
        Args:
            role: The role ("user" or "assistant")
            content: The message content
        """
        if role not in ["user", "assistant", "system"]:
            console.print(f"[bold red]Invalid role: {role}. Must be 'user', 'assistant', or 'system'.[/bold red]")
            return
            
        self.conversation_history.append({"role": role, "content": content})
        
    def clear_history(self):
        """
        Clear the conversation history.
        """
        self.conversation_history = []
        console.print("[green]Conversation history cleared.[/green]")
        
    def save_history(self, filename: str = None):
        """
        Save the conversation history to a file.
        
        Args:
            filename: Optional filename to save to
        """
        if not self.conversation_history:
            console.print("[yellow]No conversation history to save.[/yellow]")
            return
            
        if not filename:
            
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"conversation-{timestamp}.json"
            
       
        if not filename.endswith(".json"):
            filename += ".json"
            
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.conversation_history, f, indent=2)
                
            console.print(f"[green]Conversation history saved to {filename}[/green]")
        except Exception as e:
            console.print(f"[bold red]Error saving conversation history: {e}[/bold red]")
            
    def load_history(self, filename: str):
        """
        Load conversation history from a file.
        
        Args:
            filename: The filename to load from
        """
        if not os.path.exists(filename):
            console.print(f"[bold red]File {filename} does not exist.[/bold red]")
            return
            
        try:
            with open(filename, "r", encoding="utf-8") as f:
                history = json.load(f)
                
           
            if not all(isinstance(msg, dict) and "role" in msg and "content" in msg for msg in history):
                console.print("[bold red]Invalid conversation history format.[/bold red]")
                return
                
            self.conversation_history = history
            console.print(f"[green]Loaded {len(history)} messages from {filename}[/green]")
        except Exception as e:
            console.print(f"[bold red]Error loading conversation history: {e}[/bold red]")