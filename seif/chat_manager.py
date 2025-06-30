from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.markdown import Markdown
from rich.status import Status
from rich.prompt import Prompt
import time

from .llm import LLM
from .memory import Memory
from .config import config

console = Console()

class ChatManager:
    """Manages chat interactions with enhanced memory and response handling.
    
    This class provides a structured way to handle chat interactions, including:
    - Conversation memory management
    - Response generation with appropriate system prompts
    - Command recognition and handling
    - Chat history persistence
    """
    
    def __init__(self, model: Optional[str] = None):
        """Initialize the chat manager.
        
        Args:
            model: Optional model name to use for the LLM
        """
        self.llm = LLM(model=model)
        self.memory = Memory()
        self.system_prompt = self._get_system_prompt()
        
        self.memory.add_message("system", self.system_prompt)
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt from config or use default."""
        default_prompt = """
        You are SeifCLI, a helpful AI assistant with browser automation capabilities.
        You can help users with information and suggest browser automation tasks.
        When users want to perform browser tasks, suggest using the 'task:' prefix.
        Be concise, helpful, and friendly.
        """
        
        return config.get("chat", "system_prompt", default_prompt)
    
    def process_input(self, user_input: str) -> Dict[str, Any]:
        """Process user input and determine the appropriate action.
        
        Args:
            user_input: The user's input text
            
        Returns:
            A dictionary with action type and relevant data
        """
        if user_input.lower() in ['exit', 'quit', 'bye']:
            return {"action": "exit"}
            
        elif user_input.lower() == 'help':
            return {"action": "help"}
            
        elif user_input.lower() == 'clear':
            return {"action": "clear"}
            
        elif user_input.lower() == 'clear history':
            self.memory.clear()
            return {"action": "message", "content": "Conversation history cleared."}
            
        elif user_input.lower().startswith('save history'):
            parts = user_input.split(' ', 2)
            filename = parts[2] if len(parts) > 2 else None
            saved_path = self.memory.save(filename)
            
            if saved_path:
                return {"action": "message", "content": f"Conversation history saved to {saved_path}"}
            else:
                return {"action": "message", "content": "Failed to save conversation history."}
                
        elif user_input.lower().startswith('load history'):
            parts = user_input.split(' ', 2)
            if len(parts) <= 2:
                return {"action": "message", "content": "Please specify a filename to load."}
                
            success = self.memory.load(parts[2])
            if success:
                return {"action": "message", "content": "Conversation history loaded successfully."}
            else:
                return {"action": "message", "content": "Failed to load conversation history."}
                
        elif user_input.lower().startswith('task:'):
            task = user_input[5:].strip()
            return {"action": "task", "content": task}
        
        self.memory.add_message("user", user_input)
        
        return {"action": "chat", "content": user_input}
    
    def generate_response(self, user_input: str) -> str:
        """Generate a response to the user input.
        
        Args:
            user_input: The user's input text
            
        Returns:
            The generated response
        """
        context = self.memory.get_formatted_context()
        
        with console.status("[bold green]Thinking...[/bold green]", spinner="dots") as status:
            response = self.llm.generate(
                prompt=user_input,
                system_prompt=self.system_prompt,
                with_history=True
            )
        
        self.memory.add_message("assistant", response)
        
        return response
    
    def display_response(self, response: str) -> None:
        """Display the response to the user.
        
        Args:
            response: The response text
        """
        console.print(f"[bold green]🤖 Assistant:[/bold green]")
        console.print(Markdown(response))
    
    def list_sessions(self) -> None:
        """List all saved chat sessions."""
        sessions = self.memory.list_sessions()
        
        if not sessions:
            console.print("[yellow]No saved sessions found.[/yellow]")
            return
        
        console.print("[bold]Saved Chat Sessions:[/bold]")
        for i, session in enumerate(sessions, 1):
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(session["created_at"]))
            
            tags = ", ".join(session["tags"]) if session["tags"] else "No tags"
            
            console.print(f"[bold]{i}.[/bold] {session['filename']}")
            console.print(f"   Created: {timestamp}")
            console.print(f"   Messages: {session['message_count']}")
            console.print(f"   Tags: {tags}")
            console.print("")
    
    def tag_current_session(self, tag: str) -> None:
        """Add a tag to the current session.
        
        Args:
            tag: The tag to add
        """
        self.memory.add_tag(tag)
        console.print(f"[green]Added tag: {tag}[/green]")