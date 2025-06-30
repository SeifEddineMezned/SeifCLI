import json
import os
import time
from pathlib import Path
from typing import List, Dict, Optional, Any
from rich.console import Console
from rich.prompt import Confirm


from .config import config

console = Console()

class Memory:
    """Advanced conversation memory management for SeifCLI.
    
    This class provides enhanced memory capabilities beyond the basic conversation
    history in the LLM class, including:
    - Persistent storage of conversations
    - Summarization of long conversations
    - Tagging and searching conversations
    - Memory pruning for context window management
    """
    
    def __init__(self):
        """Initialize the memory system."""
        self.memory_dir = self._get_memory_dir()
        self.current_session = {
            "id": time.strftime("%Y%m%d-%H%M%S"),
            "created_at": time.time(),
            "messages": [],
            "summary": "",
            "tags": []
        }
        self.max_context_length = config.get("memory", "max_context_length", 4000)
        self.auto_summarize = config.get("memory", "auto_summarize", True)
        self.summarize_threshold = config.get("memory", "summarize_threshold", 10)
    
    def _get_memory_dir(self) -> Path:
        """Get the directory for storing memory files."""
        memory_dir = Path(config.get_config_dir()) / "memory"
        memory_dir.mkdir(parents=True, exist_ok=True)
        return memory_dir
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the current session.
        
        Args:
            role: The role of the message sender ("user", "assistant", "system")
            content: The content of the message
        """
        if role not in ["user", "assistant", "system"]:
            console.print(f"[bold red]Invalid role: {role}. Must be 'user', 'assistant', or 'system'.[/bold red]")
            return
        
        message = {
            "role": role,
            "content": content,
            "timestamp": time.time()
        }
        
        self.current_session["messages"].append(message)
        
        if (self.auto_summarize and 
            len(self.current_session["messages"]) % self.summarize_threshold == 0):
            self._summarize_session()
    
    def get_messages(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get messages from the current session.
        
        Args:
            limit: Optional limit on the number of most recent messages to return
            
        Returns:
            List of message dictionaries
        """
        if limit is None:
            return self.current_session["messages"]
        return self.current_session["messages"][-limit:]
    
    def get_formatted_context(self, include_summary: bool = True) -> List[Dict[str, str]]:
        """Get the current context formatted for LLM consumption.
        
        Args:
            include_summary: Whether to include the session summary
            
        Returns:
            List of message dictionaries in the format expected by LLMs
        """
        context = []
        
        if include_summary and self.current_session["summary"]:
            context.append({
                "role": "system", 
                "content": f"Previous conversation summary: {self.current_session['summary']}"
            })
        
        total_length = sum(len(msg["content"]) for msg in context)
        messages = []
        
        for msg in reversed(self.current_session["messages"]):
            msg_length = len(msg["content"])
            if total_length + msg_length <= self.max_context_length:
                messages.insert(0, {"role": msg["role"], "content": msg["content"]})
                total_length += msg_length
            else:
                break
        
        context.extend(messages)
        return context
    
    def clear(self) -> None:
        """Clear the current session."""
        self.current_session = {
            "id": time.strftime("%Y%m%d-%H%M%S"),
            "created_at": time.time(),
            "messages": [],
            "summary": "",
            "tags": []
        }
        console.print("[green]Memory cleared.[/green]")
    
    def save(self, filename: Optional[str] = None) -> str:
        """Save the current session to a file.
        
        Args:
            filename: Optional filename to save to
            
        Returns:
            The path to the saved file
        """
        if not self.current_session["messages"]:
            console.print("[yellow]No messages to save.[/yellow]")
            return ""
        
        if not filename:
            filename = f"session_{self.current_session['id']}.json"
        
        if not filename.endswith(".json"):
            filename += ".json"
        
        file_path = self.memory_dir / filename
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.current_session, f, indent=2)
            
            console.print(f"[green]Session saved to {file_path}[/green]")
            return str(file_path)
        except Exception as e:
            console.print(f"[bold red]Error saving session: {e}[/bold red]")
            return ""
    
    def load(self, filename: str) -> bool:
        """Load a session from a file.
        
        Args:
            filename: The filename to load from
            
        Returns:
            True if successful, False otherwise
        """
        file_path = self.memory_dir / filename if not os.path.isabs(filename) else Path(filename)
        
        if not file_path.exists():
            console.print(f"[bold red]File {file_path} does not exist.[/bold red]")
            return False
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                session = json.load(f)
            
            required_keys = ["id", "created_at", "messages"]
            if not all(key in session for key in required_keys):
                console.print("[bold red]Invalid session format.[/bold red]")
                return False
            
            if self.current_session["messages"] and not Confirm.ask(
                "Current session has unsaved messages. Load anyway?", default=False
            ):
                return False
            
            self.current_session = session
            console.print(f"[green]Loaded {len(session['messages'])} messages from {file_path}[/green]")
            return True
        except Exception as e:
            console.print(f"[bold red]Error loading session: {e}[/bold red]")
            return False
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all saved sessions.
        
        Returns:
            List of session metadata dictionaries
        """
        sessions = []
        
        for file_path in self.memory_dir.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    session = json.load(f)
                
                sessions.append({
                    "id": session.get("id", "unknown"),
                    "filename": file_path.name,
                    "created_at": session.get("created_at", 0),
                    "message_count": len(session.get("messages", [])),
                    "tags": session.get("tags", [])
                })
            except Exception:
                pass
        
        sessions.sort(key=lambda x: x["created_at"], reverse=True)
        return sessions
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the current session.
        
        Args:
            tag: The tag to add
        """
        if tag not in self.current_session["tags"]:
            self.current_session["tags"].append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the current session.
        
        Args:
            tag: The tag to remove
        """
        if tag in self.current_session["tags"]:
            self.current_session["tags"].remove(tag)
    
    def search_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """Search for sessions with a specific tag.
        
        Args:
            tag: The tag to search for
            
        Returns:
            List of matching session metadata dictionaries
        """
        sessions = self.list_sessions()
        return [session for session in sessions if tag in session["tags"]]
    
    def _summarize_session(self) -> None:
        """Summarize the current session using the LLM.
        
        This is called automatically when the number of messages exceeds the threshold.
        """
        if not self.current_session["messages"]:
            return
        
       
        first_msg = self.current_session["messages"][0]["content"] if self.current_session["messages"] else ""
        last_msg = self.current_session["messages"][-1]["content"] if self.current_session["messages"] else ""
        
        self.current_session["summary"] = (
            f"Conversation with {len(self.current_session['messages'])} messages. "
            f"Started with: '{first_msg[:50]}...' and "
            f"most recently discussed: '{last_msg[:50]}...'"
        )