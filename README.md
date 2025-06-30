# 🤖 SeifCLI

<div align="center">

![SeifCLI Logo](https://img.shields.io/badge/SeifCLI-AI%20Terminal%20Assistant-blueviolet?style=for-the-badge&logo=terminal&logoColor=white)

**Your smart terminal assistant — powered by local LLMs, styled with Rich, and able to control your browser like a personal hacker butler** 🕴️

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-green?style=flat-square&logo=llama&logoColor=white)](https://ollama.ai)
[![Rich](https://img.shields.io/badge/Rich-Beautiful%20Terminal-orange?style=flat-square&logo=python&logoColor=white)](https://rich.readthedocs.io)
[![Selenium](https://img.shields.io/badge/Selenium-Browser%20Automation-yellow?style=flat-square&logo=selenium&logoColor=white)](https://selenium.dev)

</div>

---

## 🌟 What is SeifCLI?

SeifCLI is a **proof-of-concept AI-powered command-line assistant** that bridges the gap between natural language and terminal automation. It understands what you want to do in plain English and executes complex web-based tasks automatically.

> 💡 **No API keys needed by default** — runs entirely on your local machine with privacy-first design!

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🗣️ **Natural Language Interface**
- Speak to your terminal in plain English
- No need to remember complex commands
- Intuitive and conversational experience

### 🏠 **Privacy-First Design**
- Local LLMs via Ollama by default
- No data leaves your machine
- Offline capability built-in

### 🔧 **Multiple LLM Backends**
- 🦙 **Ollama** (recommended)
- 🤖 **OpenAI** (optional)
- 🔗 **llama.cpp** support
- Easy to extend for more providers

</td>
<td width="50%">

### 🌐 **Browser Automation**
- Opens and navigates websites automatically
- Interacts with web elements
- Takes screenshots and extracts data

### 🎨 **Beautiful Terminal UI**
- Rich, colorful output with progress bars
- Formatted text and interactive elements
- Professional-looking terminal experience

### 🔌 **Extensible Plugin System**
- Modular skills architecture
- Easy to add new capabilities
- Community-friendly design

</td>
</tr>
</table>

---

## 🚀 Quick Start

### 📦 Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd seifcli

# 2. Install Ollama and pull a model
# Visit https://ollama.ai/ for installation instructions
ollama pull mistral

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Optional: Configure SeifCLI
python -m main setup
```

### 🎯 Usage Examples

<details>
<summary><strong>🔥 Direct Commands</strong></summary>

```bash
# Search and screenshot
python -m main run "Search for AI news on Google and take a screenshot"

# Web scraping
python -m main run "Go to GitHub trending page and extract all repository names"

# Data extraction
python -m main run "Visit weather.com and save today's forecast to a file"
```

</details>

<details>
<summary><strong>💬 Interactive Chat Mode</strong></summary>

```bash
# Start a chat session
python -m main chat

# Chat with memory persistence
python -m main chat --save
python -m main chat --load history_file.json

# Use specific models
python -m main chat --model llama3
```

</details>

---

## 🛠️ Built-in Skills

SeifCLI comes packed with powerful skills right out of the box:

| Skill | Description | Example Usage |
|-------|-------------|---------------|
| 📸 **SCREENSHOT** | Capture web page screenshots | "Take a screenshot of the current page" |
| 📝 **EXTRACT_TEXT** | Extract text using CSS selectors | "Get all paragraph text from this article" |
| 🔗 **EXTRACT_LINKS** | Extract links from web pages | "Find all download links on this page" |
| 💾 **SAVE_TEXT** | Save content to text files | "Save this content to notes.txt" |
| 📂 **LOAD_TEXT** | Load text from files | "Load the content from my notes" |
| 📊 **SAVE_JSON** | Save structured data as JSON | "Save this data as config.json" |
| 📋 **LOAD_JSON** | Load JSON data | "Load settings from config file" |

---

## 🔧 Creating Custom Skills

Extend SeifCLI's capabilities by creating custom skills! It's as simple as adding a Python file:

```python
# seif/skills/my_custom_skill.py
from ..browser import Browser

def analyze_website_performance(browser: Browser, url: str, metrics: str = "basic"):
    """Analyze website performance metrics"""
    
    # Your custom logic here
    browser.get(url)
    # ... performance analysis code ...
    
    return {"performance_score": 95, "load_time": "1.2s"}

SKILLS = {
    "ANALYZE_PERFORMANCE": analyze_website_performance
}
```

Then use it naturally:
```bash
python -m main run "Analyze the performance of example.com"
```

---

## 🏗️ Architecture

```mermaid
graph TB
    A[User Input] --> B[Natural Language Processing]
    B --> C[LLM Backend]
    C --> D{Action Required?}
    D -->|Web Task| E[Browser Controller]
    D -->|File Operation| F[File Skills]
    D -->|Data Processing| G[Processing Skills]
    E --> H[Rich Terminal Output]
    F --> H
    G --> H
```

---

## 🤝 Contributing

We welcome contributions! SeifCLI is designed to be:
- **Modular**: Easy to add new skills and backends
- **Extensible**: Plugin architecture for community contributions
- **Well-documented**: Clear code and comprehensive docs

---

## 📄 License

[Add your license information here]

---

<div align="center">

**Made with ❤️ by developers who believe terminals should be smarter**

[⭐ Star this repo](../../stargazers) • [🐛 Report bugs](../../issues) • [💡 Request features](../../issues/new)

</div>
