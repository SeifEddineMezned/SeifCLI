# seifcli/seif/skills/file_operations.py

from rich.console import Console
import json
import csv
import os
from pathlib import Path
from rich.prompt import Confirm

console = Console()

def save_text(browser, text: str, filename: str):
    """
    Saves text to a file.
    
    Args:
        browser: The browser instance (not used but required by skill interface)
        text: Text content to save
        filename: Name of the file to save to
        
    Returns:
        A message indicating the result of the operation
    """
    try:
        # Ensure the filename has a .txt extension
        if not filename.endswith(".txt"):
            filename += ".txt"
            
        # Check if file exists and confirm overwrite
        if os.path.exists(filename):
            if not Confirm.ask(f"⚠️ File {filename} already exists. Overwrite?", default=False):
                return "Operation cancelled by user."
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
            
        console.print(f"[green]✓[/green] Text saved to {filename}")
        return f"Text saved to {filename}"
    except Exception as e:
        return f"Error saving text: {str(e)}"

def load_text(browser, filename: str):
    """
    Loads text from a file.
    
    Args:
        browser: The browser instance (not used but required by skill interface)
        filename: Name of the file to load from
        
    Returns:
        The content of the file or an error message
    """
    try:
        # Ensure the file exists
        if not os.path.exists(filename):
            return f"File {filename} does not exist."
            
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            
        console.print(f"[green]✓[/green] Loaded text from {filename}")
        
        # Display a preview of the content
        preview = content[:200] + "..." if len(content) > 200 else content
        console.print(f"[bold]Content preview:[/bold]\n{preview}")
        
        return f"Loaded text from {filename}"
    except Exception as e:
        return f"Error loading text: {str(e)}"

def save_json(browser, data: str, filename: str):
    """
    Saves data as JSON to a file.
    
    Args:
        browser: The browser instance (not used but required by skill interface)
        data: JSON string to save
        filename: Name of the file to save to
        
    Returns:
        A message indicating the result of the operation
    """
    try:
        # Ensure the filename has a .json extension
        if not filename.endswith(".json"):
            filename += ".json"
            
        # Check if file exists and confirm overwrite
        if os.path.exists(filename):
            if not Confirm.ask(f"⚠️ File {filename} already exists. Overwrite?", default=False):
                return "Operation cancelled by user."
        
        # Parse the JSON string to ensure it's valid
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            return "Invalid JSON data provided."
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)
            
        console.print(f"[green]✓[/green] JSON data saved to {filename}")
        return f"JSON data saved to {filename}"
    except Exception as e:
        return f"Error saving JSON: {str(e)}"

def load_json(browser, filename: str):
    """
    Loads JSON data from a file.
    
    Args:
        browser: The browser instance (not used but required by skill interface)
        filename: Name of the file to load from
        
    Returns:
        A message indicating the result of the operation
    """
    try:
        # Ensure the file exists
        if not os.path.exists(filename):
            return f"File {filename} does not exist."
            
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        console.print(f"[green]✓[/green] Loaded JSON data from {filename}")
        
        # Display a preview of the content
        preview = json.dumps(data, indent=2)[:200] + "..." if len(json.dumps(data)) > 200 else json.dumps(data, indent=2)
        console.print(f"[bold]Content preview:[/bold]\n{preview}")
        
        return f"Loaded JSON data from {filename}"
    except json.JSONDecodeError:
        return f"File {filename} does not contain valid JSON data."
    except Exception as e:
        return f"Error loading JSON: {str(e)}"

# Export the skills
SKILLS = {
    "SAVE_TEXT": save_text,
    "LOAD_TEXT": load_text,
    "SAVE_JSON": save_json,
    "LOAD_JSON": load_json
}