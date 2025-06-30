<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SeifCLI - Your Smart Terminal Assistant</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Orbitron:wght@400;700;900&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --bg-primary: #0f0f23;
            --bg-secondary: #1a1a40;
            --accent-green: #00ff88;
            --accent-cyan: #00ccff;
            --accent-pink: #ff00cc;
            --accent-yellow: #ffff00;
            --text-primary: #00ff88;
            --text-secondary: #00ccff;
            --text-dim: #888;
            --terminal-bg: rgba(0, 0, 0, 0.9);
            --border-glow: rgba(0, 255, 136, 0.3);
        }

        body {
            font-family: 'JetBrains Mono', monospace;
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 50%, var(--bg-primary) 100%);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Animated Background */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.1;
        }

        .bg-animation::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent, var(--accent-green), transparent);
            animation: scan 8s linear infinite;
        }

        @keyframes scan {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100vw) translateY(100vh) rotate(45deg); }
        }

        /* ASCII Art Header */
        .ascii-header {
            text-align: center;
            padding: 2rem 0;
            background: var(--terminal-bg);
            border: 3px solid var(--accent-green);
            border-radius: 15px;
            margin: 2rem 0;
            box-shadow: 
                0 0 20px var(--border-glow),
                0 0 40px rgba(0, 255, 136, 0.1),
                inset 0 0 20px rgba(0, 255, 136, 0.05);
            position: relative;
            overflow: hidden;
        }

        .ascii-header::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, var(--accent-green), var(--accent-cyan), var(--accent-pink), var(--accent-yellow), var(--accent-green));
            background-size: 400% 400%;
            border-radius: 15px;
            z-index: -1;
            animation: borderGlow 4s ease-in-out infinite;
        }

        @keyframes borderGlow {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .ascii-art {
            font-family: 'JetBrains Mono', monospace;
            font-size: 18px;
            line-height: 1.2;
            background: linear-gradient(45deg, var(--accent-green), var(--accent-cyan), var(--accent-pink));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
            animation: pulse 2s ease-in-out infinite;
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

        .tagline {
            font-size: 14px;
            color: var(--accent-cyan);
            text-shadow: 0 0 10px rgba(0, 204, 255, 0.7);
            animation: glow 3s ease-in-out infinite alternate;
            margin: 1rem 0;
        }

        @keyframes glow {
            0% { text-shadow: 0 0 10px rgba(0, 204, 255, 0.7); }
            100% { text-shadow: 0 0 20px rgba(0, 204, 255, 1), 0 0 30px rgba(0, 204, 255, 0.5); }
        }

        .decorative-line {
            color: var(--accent-green);
            text-align: center;
            margin: 15px 0;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
        }

        .sparkle {
            color: var(--accent-yellow);
            animation: sparkle 1.5s ease-in-out infinite;
        }

        @keyframes sparkle {
            0%, 100% { opacity: 0.3; transform: scale(0.8); }
            50% { opacity: 1; transform: scale(1.2); }
        }

        /* Terminal Cards */
        .terminal-card {
            background: var(--terminal-bg);
            border: 2px solid var(--accent-green);
            border-radius: 12px;
            padding: 2rem;
            margin: 2rem 0;
            position: relative;
            overflow: hidden;
            box-shadow: 
                0 0 15px var(--border-glow),
                inset 0 0 15px rgba(0, 255, 136, 0.05);
            transition: all 0.3s ease;
        }

        .terminal-card::before {
            content: '● ● ●';
            position: absolute;
            top: 0.5rem;
            left: 1rem;
            color: var(--text-dim);
            font-size: 0.8rem;
        }

        .terminal-card:hover {
            border-color: var(--accent-cyan);
            box-shadow: 
                0 0 25px rgba(0, 204, 255, 0.4),
                inset 0 0 25px rgba(0, 204, 255, 0.1);
            transform: translateY(-5px);
        }

        .terminal-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 136, 0.1), transparent);
            transition: left 0.7s ease;
        }

        .terminal-card:hover::after {
            left: 100%;
        }

        /* Section Headers */
        .section-header {
            font-family: 'Orbitron', monospace;
            font-size: 2.5rem;
            font-weight: 900;
            text-align: center;
            margin: 4rem 0 2rem;
            background: linear-gradient(45deg, var(--accent-green), var(--accent-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
            position: relative;
        }

        .section-header::before {
            content: '▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄';
            display: block;
            color: var(--accent-green);
            font-size: 0.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
        }

        .section-header::after {
            content: '▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀';
            display: block;
            color: var(--accent-green);
            font-size: 0.5rem;
            margin-top: 0.5rem;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
        }

        /* Features Grid */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }

        .feature-card {
            background: var(--terminal-bg);
            border: 2px solid var(--accent-cyan);
            border-radius: 12px;
            padding: 2rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .feature-card::before {
            content: '[' attr(data-id) ']';
            position: absolute;
            top: 0.5rem;
            right: 1rem;
            color: var(--accent-yellow);
            font-size: 0.8rem;
            font-weight: bold;
        }

        .feature-card:hover {
            border-color: var(--accent-pink);
            box-shadow: 0 0 20px rgba(255, 0, 204, 0.3);
            transform: translateY(-8px) scale(1.02);
        }

        .feature-icon {
            font-size: 2rem;
            margin-bottom: 1rem;
            color: var(--accent-green);
            text-shadow: 0 0 15px rgba(0, 255, 136, 0.8);
        }

        .feature-title {
            font-family: 'Orbitron', monospace;
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--accent-cyan);
            text-shadow: 0 0 10px rgba(0, 204, 255, 0.5);
        }

        .feature-desc {
            color: var(--text-primary);
            font-size: 0.9rem;
            line-height: 1.5;
        }

        /* Code Blocks */
        .code-block {
            background: #000;
            border: 2px solid var(--accent-green);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            position: relative;
            overflow-x: auto;
            box-shadow: 
                0 0 15px rgba(0, 255, 136, 0.2),
                inset 0 0 15px rgba(0, 255, 136, 0.05);
        }

        .code-block::before {
            content: '> ' attr(data-lang);
            position: absolute;
            top: 0.5rem;
            right: 1rem;
            background: var(--accent-green);
            color: #000;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: bold;
        }

        .code-block code {
            color: var(--accent-green);
            display: block;
            white-space: pre;
            text-shadow: 0 0 5px rgba(0, 255, 136, 0.3);
        }

        /* Installation Steps */
        .install-steps {
            margin: 2rem 0;
        }

        .install-step {
            display: flex;
            align-items: flex-start;
            margin: 2rem 0;
            padding: 2rem;
            background: var(--terminal-bg);
            border: 2px solid var(--accent-yellow);
            border-radius: 12px;
            border-left: 6px solid var(--accent-green);
            transition: all 0.3s ease;
            position: relative;
        }

        .install-step::before {
            content: '[STEP ' attr(data-step) ']';
            position: absolute;
            top: 0.5rem;
            right: 1rem;
            color: var(--accent-yellow);
            font-size: 0.8rem;
            font-weight: bold;
        }

        .install-step:hover {
            border-color: var(--accent-green);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
            transform: translateX(10px);
        }

        .step-number {
            background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
            color: #000;
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2rem;
            margin-right: 1.5rem;
            flex-shrink: 0;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
        }

        .step-content h3 {
            color: var(--accent-cyan);
            margin-bottom: 0.5rem;
            font-family: 'Orbitron', monospace;
            text-shadow: 0 0 10px rgba(0, 204, 255, 0.5);
        }

        .step-content p {
            color: var(--text-primary);
            margin-bottom: 1rem;
        }

        /* Skills */
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .skill-item {
            background: var(--terminal-bg);
            border: 2px solid var(--accent-pink);
            border-radius: 8px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            position: relative;
        }

        .skill-item::before {
            content: '◉';
            position: absolute;
            top: 0.5rem;
            left: 0.5rem;
            color: var(--accent-green);
            font-size: 0.8rem;
            animation: blink 2s infinite;
        }

        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0.3; }
        }

        .skill-item:hover {
            border-color: var(--accent-green);
            background: rgba(0, 255, 136, 0.05);
            transform: translateY(-3px);
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
        }

        .skill-name {
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            color: var(--accent-cyan);
            margin-bottom: 0.5rem;
            text-shadow: 0 0 10px rgba(0, 204, 255, 0.5);
        }

        .skill-desc {
            color: var(--text-primary);
            font-size: 0.9rem;
        }

        /* Interactive Terminal */
        .interactive-terminal {
            background: #000;
            border: 3px solid var(--accent-green);
            border-radius: 12px;
            padding: 2rem;
            margin: 2rem 0;
            font-family: 'JetBrains Mono', monospace;
            position: relative;
            box-shadow: 
                0 0 20px var(--border-glow),
                inset 0 0 20px rgba(0, 255, 136, 0.05);
        }

        .interactive-terminal::before {
            content: 'SEIF-CLI v1.0.0 - INTERACTIVE DEMO';
            position: absolute;
            top: 0.5rem;
            left: 1rem;
            color: var(--accent-yellow);
            font-size: 0.8rem;
            font-weight: bold;
        }

        .terminal-line {
            margin: 0.8rem 0;
            padding-top: 1.5rem;
            display: flex;
            align-items: center;
        }

        .prompt {
            color: var(--accent-green);
            margin-right: 0.5rem;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
        }

        .command {
            color: var(--accent-cyan);
            text-shadow: 0 0 10px rgba(0, 204, 255, 0.8);
        }

        .output {
            color: var(--accent-yellow);
            text-shadow: 0 0 10px rgba(255, 255, 0, 0.8);
        }

        .cursor {
            background: var(--accent-green);
            color: #000;
            padding: 0 0.2rem;
            animation: blink 1s infinite;
        }

        /* Demo Button */
        .demo-button {
            background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
            color: #000;
            border: none;
            padding: 1rem 2rem;
            border-radius: 8px;
            font-weight: bold;
            font-size: 1rem;
            font-family: 'Orbitron', monospace;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 1rem;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
            text-transform: uppercase;
        }

        .demo-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 25px rgba(0, 255, 136, 0.8);
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-pink));
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container { padding: 0 1rem; }
            .ascii-art { font-size: 12px; }
            .section-header { font-size: 2rem; }
            .features-grid { grid-template-columns: 1fr; }
            .terminal-card { padding: 1.5rem; }
        }

        /* Scroll Animation */
        .fade-in {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.8s ease;
        }

        .fade-in.visible {
            opacity: 1;
            transform: translateY(0);
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 4rem 0 2rem;
            color: var(--text-dim);
            border-top: 1px solid var(--accent-green);
            margin-top: 4rem;
        }

        .footer .sparkle {
            color: var(--accent-pink);
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    
    <div class="container">
        <!-- ASCII Art Header -->
        <div class="ascii-header fade-in">
            <pre class="ascii-art">
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
            
            <pre class="tagline">
┌─────────────────────────────────────────────────────────┐
│    🚀 Your smart terminal assistant — powered by AI 🚀   │
│       Local LLMs • Browser Control • No API Keys       │
└─────────────────────────────────────────────────────────┘
            </pre>
            
            <div class="decorative-line">
                <span class="sparkle">✧</span> ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ <span class="sparkle">✧</span>
            </div>
        </div>

        <!-- Description -->
        <div class="terminal-card fade-in">
            <p style="padding-top: 1rem; font-size: 1.1rem; line-height: 1.8;">
                SeifCLI is a proof-of-concept AI-powered command-line assistant that understands natural language and automates web-based tasks. It uses local Large Language Models (LLMs) to interpret your commands, Selenium to control a web browser, and Rich to provide beautiful, interactive terminal output.
            </p>
        </div>

        <!-- Interactive Demo -->
        <div class="interactive-terminal fade-in">
            <div class="terminal-line">
                <span class="prompt">seif@terminal:~$</span>
                <span class="command">python -m main run "Search for AI news on Google"</span>
                <span class="cursor">█</span>
            </div>
            <div class="terminal-line">
                <span class="output">🤖 [AI-CORE] Understanding your request...</span>
            </div>
            <div class="terminal-line">
                <span class="output">🌐 [BROWSER] Opening browser and navigating to Google...</span>
            </div>
            <div class="terminal-line">
                <span class="output">✨ [SUCCESS] Task completed successfully!</span>
            </div>
            <div style="text-align: center; margin-top: 2rem;">
                <button class="demo-button" onclick="animateTerminal()">RUN DEMO</button>
            </div>
        </div>

        <!-- Features -->
        <section class="fade-in">
            <h2 class="section-header">SYSTEM FEATURES</h2>
            <div class="features-grid">
                <div class="feature-card" data-id="NLP">
                    <div class="feature-icon">🗣️</div>
                    <h3 class="feature-title">Natural Language Commands</h3>
                    <p class="feature-desc">Simply tell SeifCLI what to do in plain English. No complex syntax or memorizing commands required.</p>
                </div>
                <div class="feature-card" data-id="LOCAL">
                    <div class="feature-icon">🏠</div>
                    <h3 class="feature-title">Local First AI</h3>
                    <p class="feature-desc">Powered by local LLMs like Ollama, ensuring privacy and offline capability. No API keys required by default.</p>
                </div>
                <div class="feature-card" data-id="MULTI">
                    <div class="feature-icon">🔄</div>
                    <h3 class="feature-title">Multiple LLM Backends</h3>
                    <p class="feature-desc">Support for Ollama, OpenAI, and llama.cpp with easy extensibility for more providers.</p>
                </div>
                <div class="feature-card" data-id="BROWSER">
                    <div class="feature-icon">🌐</div>
                    <h3 class="feature-title">Browser Automation</h3>
                    <p class="feature-desc">Can open, navigate, and interact with websites to perform complex tasks automatically.</p>
                </div>
                <div class="feature-card" data-id="UI">
                    <div class="feature-icon">✨</div>
                    <h3 class="feature-title">Rich Terminal UI</h3>
                    <p class="feature-desc">Beautiful and informative output with progress indicators, formatted text, and more.</p>
                </div>
                <div class="feature-card" data-id="CHAT">
                    <div class="feature-icon">💬</div>
                    <h3 class="feature-title">Interactive Chat Mode</h3>
                    <p class="feature-desc">A conversational interface with memory and history management for extended sessions.</p>
                </div>
                <div class="feature-card" data-id="SKILLS">
                    <div class="feature-icon">🧩</div>
                    <h3 class="feature-title">Extensible Skills System</h3>
                    <p class="feature-desc">A modular plugin system that allows for new capabilities to be added easily.</p>
                </div>
                <div class="feature-card" data-id="SECURE">
                    <div class="feature-icon">🔒</div>
                    <h3 class="feature-title">Security Conscious</h3>
                    <p class="feature-desc">Asks for confirmation before performing potentially sensitive actions.</p>
                </div>
            </div>
        </section>

        <!-- Installation -->
        <section class="fade-in">
            <h2 class="section-header">INSTALLATION PROTOCOL</h2>
            <div class="install-steps">
                <div class="install-step" data-step="01">
                    <div class="step-number">1</div>
                    <div class="step-content">
                        <h3>Clone Repository</h3>
                        <p>Download the latest version of SeifCLI from the repository</p>
                        <div class="code-block" data-lang="bash">
                            <code>git clone &lt;repository-url&gt;
cd seifcli</code>
                        </div>
                    </div>
                </div>
                <div class="install-step" data-step="02">
                    <div class="step-number">2</div>
                    <div class="step-content">
                        <h3>Install Ollama</h3>
                        <p>Setup local LLM backend and download a model</p>
                        <div class="code-block" data-lang="bash">
                            <code>ollama pull mistral</code>
                        </div>
                    </div>
                </div>
                <div class="install-step" data-step="03">
                    <div class="step-number">3</div>
                    <div class="step-content">
                        <h3>Install Dependencies</h3>
                        <p>Install all required Python packages</p>
                        <div class="code-block" data-lang="bash">
                            <code>pip install -r requirements.txt</code>
                        </div>
                    </div>
                </div>
                <div class="install-step" data-step="04">
                    <div class="step-number">4</div>
                    <div class="step-content">
                        <h3>Initialize System</h3>
                        <p>Configure SeifCLI with your preferences</p>
                        <div class="code-block" data-lang="bash">
                            <code>python -m main setup</code>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Usage -->
        <section class="fade-in">
            <h2 class="section-header">USAGE PROTOCOLS</h2>
            <div class="terminal-card">
                <h3 style="color: var(--accent-cyan); margin-bottom: 1rem; font-family: 'Orbitron', monospace;">Direct Command Execution</h3>
                <div class="code-block" data-lang="bash">
                    <code>python -m main run "Search for AI news on Google and take a screenshot."</code>
                </div>
            </div>
            <div class="terminal-card">
                <h3 style="color: var(--accent-cyan); margin-bottom: 1rem; font-family: 'Orbitron', monospace;">Interactive Chat Session</h3>
                <div class="code-block" data-lang="bash">
                    <code>python -m main chat</code>
                </div>
            </div>
            <div class="terminal-card">
                <h3 style="color: var(--accent-cyan); margin-bottom: 1rem; font-family: 'Orbitron', monospace;">Persistent Memory Mode</h3>
                <div class="code-block" data-lang="bash">
                    <code>python -m main chat --


ChatGPT said:
css
Copy
Edit
                --save
python -m main chat --load history_file.json
</code>
</div>
</div>
<div class="terminal-card">
<h3 style="color: var(--accent-cyan); margin-bottom: 1rem; font-family: 'Orbitron', monospace;">Using Specific Model</h3>
<div class="code-block" data-lang="bash">
<code>python -m main chat --model llama3
python -m main run "Search for Python tutorials" --model mistral</code>
</div>
</div>
</section>

php-template
Copy
Edit
    <!-- Skills Section -->
    <section class="fade-in">
        <h2 class="section-header">AVAILABLE SKILLS</h2>
        <div class="skills-grid">
            <div class="skill-item">
                <h4 class="skill-name">SCREENSHOT</h4>
                <p class="skill-desc">Take screenshots of web pages in real time using browser automation.</p>
            </div>
            <div class="skill-item">
                <h4 class="skill-name">EXTRACT_TEXT</h4>
                <p class="skill-desc">Extract text content from web pages using CSS selectors.</p>
            </div>
            <div class="skill-item">
                <h4 class="skill-name">EXTRACT_LINKS</h4>
                <p class="skill-desc">Extract and parse all valid links from any webpage you visit.</p>
            </div>
            <div class="skill-item">
                <h4 class="skill-name">SAVE_TEXT / LOAD_TEXT</h4>
                <p class="skill-desc">Save or load textual data to and from local files easily.</p>
            </div>
            <div class="skill-item">
                <h4 class="skill-name">SAVE_JSON / LOAD_JSON</h4>
                <p class="skill-desc">Persist and retrieve structured JSON data using built-in skills.</p>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer fade-in">
        <p>Built with <span class="sparkle">✦</span> by <strong>Seif Eddine Mezned</strong> | <code>SeifCLI</code> v1.0.0</p>
        <p>Open-source — MIT License</p>
    </footer>
</div>

<!-- Simple Intersection Observer to Trigger Fade-in -->
<script>
    const fadeIns = document.querySelectorAll('.fade-in');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    fadeIns.forEach(el => observer.observe(el));

    // Terminal demo animation simulation (mock)
    function animateTerminal() {
        const lines = document.querySelectorAll('.interactive-terminal .terminal-line');
        lines.forEach((line, index) => {
            line.style.opacity = '0';
            setTimeout(() => {
                line.style.opacity = '1';
            }, index * 600);
        });
    }
</script>
</body> </html> ```
