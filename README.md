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
