from rich.console import Console
from rich.text import Text

def display_startup_ui():
    """Displays the visually rich startup UI without overlap."""
    console = Console()
    console.clear()

    
    console.print("\n") 
    console.print("\n")
    console.print("\n")
    console.print("\n")
    console.print("\n") 
    
    main_title_art = r"""
 ███████╗███████╗██╗███████╗     ██████╗██╗     ██╗
 ██╔════╝██╔════╝██║██╔════╝    ██╔════╝██║     ██║
 ███████╗█████╗  ██║█████╗      ██║     ██║     ██║
 ╚════██║██╔══╝  ██║██╔══╝      ██║     ██║     ██║
 ███████║███████╗██║██║         ╚██████╗███████╗██║
 ╚══════╝╚══════╝╚═╝╚═╝          ╚═════╝╚══════╝╚═╝
    """
    main_title_text = Text(main_title_art, style="bold cyan", justify="center")
    console.print(main_title_text)

   
    line1 = Text.from_markup("[yellow]✦[/yellow][dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim][yellow]✦[/yellow]", justify="center")
    console.print(line1)

    
    subtitle_art = r"""
┌─────────────────────────────────────────────────────────┐
│                  ⚡ SEIF CLI ⚡                           │
│            🚀 Command Line Interface 🚀                 │
│                  ── Power Tools ──                      │
└─────────────────────────────────────────────────────────┘
    """
    subtitle_text = Text(subtitle_art, style="bold blue", justify="center")
    console.print(subtitle_text)

    
    footer = Text.from_markup("[yellow]⭐[/yellow][dim] ──────────── Made with ♥ ──────────── [/dim][yellow]⭐[/yellow]", justify="center")
    console.print(footer)
    console.print()  

def display_banner():
    """Displays a welcome banner for the CLI."""
    console = Console()
    text = Text("SeifCLI", style="bold magenta", justify="center")
    panel = Panel(text, title="Welcome", border_style="green")
    console.print(panel)
