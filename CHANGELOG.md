# Changelog

All notable changes to SeifCLI will be documented in this file.

## [0.2.0] - 2023-07-15

### Added
- Multiple LLM backend support (Ollama, OpenAI, llama.cpp)
- Conversation memory system with persistence
- Chat history management (save/load functionality)
- Advanced memory management with tagging and search capabilities
- ChatManager for structured chat interactions
- Configuration system for customizing SeifCLI behavior
- Setup command for initial configuration

### Changed
- Enhanced LLM class with provider-specific generation methods
- Improved Agent and Planner classes to work with the enhanced LLM
- Updated main.py to integrate ChatManager and memory features
- Expanded README with new features and usage examples

### Fixed
- Various code improvements and optimizations

## [0.1.0] - 2023-06-01

### Added
- Initial release of SeifCLI
- Natural language command processing
- Browser automation with Selenium
- Rich terminal UI
- Interactive chat mode
- Basic skills system
- Security confirmation for sensitive actions