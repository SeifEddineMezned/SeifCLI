<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEIF CLI ASCII Art</title>
    <style>
        body {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a40 50%, #0f0f23 100%);
            margin: 0;
            padding: 20px;
            font-family: 'Courier New', monospace;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow-x: auto;
        }
        
        .ascii-container {
            background: rgba(0, 0, 0, 0.8);
            border: 3px solid #00ff88;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 
                0 0 20px rgba(0, 255, 136, 0.3),
                0 0 40px rgba(0, 255, 136, 0.1),
                inset 0 0 20px rgba(0, 255, 136, 0.05);
            position: relative;
            overflow: hidden;
        }
        
        .ascii-container::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #00ff88, #00ccff, #ff00cc, #ffff00, #00ff88);
            background-size: 400% 400%;
            border-radius: 15px;
            z-index: -1;
            animation: borderGlow 4s ease-in-out infinite;
        }
        
        @keyframes borderGlow {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .main-title {
            font-size: 18px;
            line-height: 1.2;
            text-align: center;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #00ff88, #00ccff, #ff00cc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
            animation: pulse 2s ease-in-out infinite;
        }
        
        .subtitle {
            font-size: 14px;
            line-height: 1.2;
            text-align: center;
            margin-bottom: 30px;
            color: #00ccff;
            text-shadow: 0 0 10px rgba(0, 204, 255, 0.7);
            animation: glow 3s ease-in-out infinite alternate;
        }
        
        .stylized-version {
            font-size: 16px;
            line-height: 1.2;
            text-align: center;
            margin-top: 30px;
            background: linear-gradient(90deg, #ff00cc, #ffff00, #00ff88, #00ccff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: rainbow 3s linear infinite;
        }
        
        @keyframes pulse {
            0%, 100% { 
                transform: scale(1);
                filter: brightness(1);
            }
            50% { 
                transform: scale(1.02);
                filter: brightness(1.2);
            }
        }
        
        @keyframes glow {
            0% { text-shadow: 0 0 10px rgba(0, 204, 255, 0.7); }
            100% { text-shadow: 0 0 20px rgba(0, 204, 255, 1), 0 0 30px rgba(0, 204, 255, 0.5); }
        }
        
        @keyframes rainbow {
            0% { background-position: 0% 50%; }
            100% { background-position: 200% 50%; }
        }
        
        .decorative-line {
            color: #00ff88;
            text-align: center;
            margin: 15px 0;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
        }
        
        .sparkle {
            color: #ffff00;
            animation: sparkle 1.5s ease-in-out infinite;
        }
        
        @keyframes sparkle {
            0%, 100% { opacity: 0.3; transform: scale(0.8); }
            50% { opacity: 1; transform: scale(1.2); }
        }
    </style>
</head>
<body>
    <div class="ascii-container">
        <pre class="main-title">
 ███████╗███████╗██╗███████╗     ██████╗██╗     ██╗
 ██╔════╝██╔════╝██║██╔════╝    ██╔════╝██║     ██║
 ███████╗█████╗  ██║█████╗      ██║     ██║     ██║
 ╚════██║██╔══╝  ██║██╔══╝      ██║     ██║     ██║
 ███████║███████╗██║██║         ╚██████╗███████╗██║
 ╚══════╝╚══════╝╚═╝╚═╝          ╚═════╝╚══════╝╚═╝
        </pre>
        
        <div class="decorative-line">
            <span class="sparkle">✦</span>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<span class="sparkle">✦</span>
        </div>
        
        <pre class="subtitle">
┌─────────────────────────────────────────────────────────┐
│                  ⚡ SEIF CLI ⚡                         │
│            🚀 Command Line Interface 🚀                │
│                  ── Power Tools ──                     │
└─────────────────────────────────────────────────────────┘
        </pre>
        
        <div class="decorative-line">
            <span class="sparkle">✧</span> ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ <span class="sparkle">✧</span>
        </div>
        
        <pre class="stylized-version">
    ████████  ████████  ████  ████████      ████████  ████      ████
   ████      ████       ████  ████         ████       ████      ████
   ████████  ████████   ████  ████████     ████       ████      ████
         ████ ████       ████  ████         ████       ████      ████
   ████████  ████████   ████  ████          ████████  ████████  ████

         ╔═══════════════════════════════════════════════════╗
         ║  ⚡ SEIF • COMMAND • LINE • INTERFACE ⚡  ║
         ╚═══════════════════════════════════════════════════╝
        </pre>
        
        <div class="decorative-line">
            <span class="sparkle">⭐</span> ──────────── Made with ♥ ──────────── <span class="sparkle">⭐</span>
        </div>
    </div>
</body>
</html>
# SeifCLI

**SeifCLI is your smart terminal assistant — powered by local LLMs, styled with Rich, and able to control your browser and execute tasks like a personal hacker butler, with no API keys needed.**

SeifCLI is a proof-of-concept AI-powered command-line assistant that understands natural language and automates web-based tasks. It uses local Large Language Models (LLMs) to interpret your commands, Selenium to control a web browser, and Rich to provide beautiful, interactive terminal output.

## Features 

-   **Natural Language Commands**: Simply tell SeifCLI what to do in plain English.
-   **Local First AI**: Powered by local LLMs like Ollama, ensuring privacy and offline capability. No API keys required by default.
-   **Multiple LLM Backends**: Support for Ollama, OpenAI, and llama.cpp (with easy extensibility for more).
-   **Browser Automation**: Can open, navigate, and interact with websites to perform tasks.
-   **Rich Terminal UI**: Beautiful and informative output with progress indicators, formatted text, and more.
-   **Interactive Chat Mode**: A conversational interface with memory and history management.
-   **Extensible Skills System**: A modular plugin system that allows for new capabilities to be added easily.
-   **Web Scraping**: Extract text and links from web pages with built-in skills.
-   **File Operations**: Save and load text and JSON data with dedicated skills.
-   **Configuration System**: Customize SeifCLI's behavior through a flexible configuration system.
-   **Security Conscious**: Asks for confirmation before performing potentially sensitive actions.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd seifcli
    ```

2.  **Install Ollama:**
    Make sure you have [Ollama](https://ollama.ai/) installed and running. You'll also need to pull a model. We recommend starting with `mistral` or `llama3`.
    ```bash
    ollama pull mistral
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Setup (optional):**
    Run the setup command to configure SeifCLI with your preferences:
    ```bash
    python -m main setup
    ```

## Usage

### Run a command directly

```bash
python -m main run "Search for AI news on Google and take a screenshot."
```

### Start an interactive chat session

```bash
python -m main chat
```

### Chat with conversation memory

```bash
python -m main chat --save 
python -m main chat --load history_file.json 
```

### Use a specific LLM model or provider

```bash
python -m main chat --model llama3
python -m main run "Search for Python tutorials" --model mistral
```

## Available Skills

SeifCLI comes with several built-in skills:

- **SCREENSHOT**: Take screenshots of web pages
- **EXTRACT_TEXT**: Extract text content from web pages using CSS selectors
- **EXTRACT_LINKS**: Extract links from web pages
- **SAVE_TEXT**: Save text content to a file
- **LOAD_TEXT**: Load text content from a file
- **SAVE_JSON**: Save data as JSON
- **LOAD_JSON**: Load data from JSON files

## Creating Custom Skills

You can easily extend SeifCLI by creating custom skills. Add a new Python file in the `seif/skills/` directory:

```python

from ..browser import Browser

def my_awesome_function(browser: Browser, arg1: str, arg2: str = None):
    """Description of what this skill does"""
    
    return "Result of the skill"


SKILLS = {
    "MY_AWESOME_SKILL": my_awesome_function
}
```
