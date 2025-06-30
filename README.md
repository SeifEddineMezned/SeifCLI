🚀 SeifCLI – Your Smart Terminal Assistant
────────────────────────────────────────────

<p align="center"> <img src="https://img.shields.io/badge/Local%20LLM-Ollama-green?style=for-the-badge&logo=OpenAI" /> <img src="https://img.shields.io/badge/Made%20With-Python-blue?style=for-the-badge&logo=python" /> <img src="https://img.shields.io/badge/UI-Rich-brightgreen?style=for-the-badge" /> <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" /> </p> <p align="center"> <img src="https://user-images.githubusercontent.com/your-gif-demo.gif" width="650" alt="SeifCLI Terminal Demo" /> </p>
🧠 SeifCLI is your hacker-butler style AI terminal assistant powered by local LLMs like Mistral or LLaMA3 via Ollama, with built-in browser control, zero API keys, and stunning Rich terminal output.

🔧 Features
─────────────────────────────

✅ Natural Language Command Execution
✅ Works Offline with Local LLMs (Ollama, llama.cpp)
✅ Browser Control via Selenium
✅ Modular "Skills" System
✅ Rich-powered CLI Output
✅ Interactive Chat with Memory
✅ Supports OpenAI & Other Backends
✅ Secure (Prompts Before Sensitive Actions)

📦 Installation
─────────────────────────────

⚙️ Clone the repo

bash
Copy
Edit
git clone https://github.com/SeifEddineMezned/SeifCLI.git
cd SeifCLI
🧠 Install Ollama and pull a model

bash
Copy
Edit
ollama pull mistral
📦 Install Python dependencies

bash
Copy
Edit
pip install -r requirements.txt
🛠️ Setup configuration

bash
Copy
Edit
python -m main setup
🕹️ Usage
─────────────────────────────

▶️ Run direct command

bash
Copy
Edit
python -m main run "Search for AI news on Google and take a screenshot."
💬 Start interactive chat

bash
Copy
Edit
python -m main chat
💾 With memory support

bash
Copy
Edit
python -m main chat --save
python -m main chat --load your_file.json
🧠 Change LLM model/provider

bash
Copy
Edit
python -m main chat --model llama3
🧩 Built-in Skills
─────────────────────────────

Skill	Description
SCREENSHOT	Takes webpage screenshots
EXTRACT_TEXT	Extracts text using CSS selectors
EXTRACT_LINKS	Extracts hyperlinks from pages
SAVE_TEXT	Saves text to file
LOAD_TEXT	Loads text from file
SAVE_JSON	Dumps JSON to file
LOAD_JSON	Loads JSON data from file

🔌 Create Your Own Skills
─────────────────────────────

Just add a file inside seif/skills/ like this:

python
Copy
Edit
from ..browser import Browser

def greet(browser: Browser, name: str):
    return f"Hello, {name}!"

SKILLS = {
    "GREET": greet
}
🌐 Project Structure
─────────────────────────────

📁 seif/ – Core logic
📁 seif/skills – Modular skill plugins
📄 main.py – Entry point
📄 requirements.txt – Dependencies
📄 config.example.json – Config template

💡 Why SeifCLI?
─────────────────────────────

⚡ Fast local inference using Ollama

🔐 100% private (no external APIs by default)

🖥️ Terminal interface feels like a real AI hacker tool

🔌 Easily extensible with new "skills"

✨ Great for demos, automating workflows, or fun experimentation

🤝 Contributing
─────────────────────────────

Got ideas or want to add a skill? Fork it, build it, and open a PR!

📜 License
─────────────────────────────

MIT License © Seif Eddine Mezned

🔥 Star this repo if you like it!

<p align="center"> <img src="https://img.shields.io/github/stars/SeifEddineMezned/SeifCLI?style=social" /> </p>
