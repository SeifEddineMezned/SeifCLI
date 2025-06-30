# This file enables the skills directory to be treated as a package
# and allows dynamic loading of skills

"""
Skills module for SeifCLI.

This package contains various skills that can be used by the SeifCLI agent.
Skills are dynamically loaded at runtime and can be easily extended.

To create a new skill:
1. Create a new Python file in this directory
2. Define functions that implement the skill
3. Export a SKILLS dictionary mapping command names to functions

Example:
    def my_skill(browser, arg1, arg2):
        # Implement skill logic here
        return "Result of skill execution"
        
    SKILLS = {
        "MY_COMMAND": my_skill
    }
"""