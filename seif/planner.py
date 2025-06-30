from .llm import LLM
from rich.console import Console
import re

console = Console()

class Planner:
    def __init__(self, model: str = None):
        self.llm = LLM(model=model)

    def create_plan(self, prompt: str) -> list[str]:
        """
        Creates a sequence of executable steps from a natural language prompt.
        """
        system_prompt = """
You are a task planner for an AI assistant. Your job is to break down a user's command into a series of precise, executable steps.
The available commands are:
- GOTO "<url>"
- TYPE "<css_selector>" "<text>"
- CLICK "<css_selector>"
- SCROLL "<direction>"  (direction can be "up" or "down")
- SCREENSHOT "<filename>"
- DONE

Guidelines:
- Think step-by-step.
- Always use the exact command format.
- Use double quotes for all arguments.
- For the TYPE command, find a specific CSS selector for the input field.
- For the CLICK command, find a specific CSS selector for the button or link.
- The final step must always be DONE.

Example:
User command: Search for trending startups on ProductHunt and screenshot the page.
Plan:
1. GOTO "https://www.producthunt.com"
2. TYPE "input[name='q']" "trending startups"
3. CLICK "button[type='submit']"
4. SCREENSHOT "producthunt_results.png"
5. DONE
"""
        with console.status("[bold magenta]Asking LLM to create a plan...", spinner="dots"):
            raw_plan = self.llm.generate(prompt, system_prompt=system_prompt)
        
        console.print("[bold green]LLM has generated a plan:[/bold green]")
        console.print(raw_plan)

        plan = re.findall(r'^\d+\.\s*(GOTO|TYPE|CLICK|SCROLL|SCREENSHOT|DONE.*)', raw_plan, re.MULTILINE)
        
        plan = []
        for line in raw_plan.strip().split('\n'):
            line = line.strip()
            if re.match(r'^\d+\.', line):
                match = re.search(r'\d+\.\s*(.*)', line)
                if match:
                    plan.append(match.group(1).strip())

        if not plan or plan[-1] != "DONE":
             console.print("[bold red]Warning: The generated plan is malformed or incomplete.[/bold red]")
        
        return plan