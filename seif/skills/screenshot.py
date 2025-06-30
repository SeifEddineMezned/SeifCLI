# seifcli/seif/skills/screenshot.py

def take_screenshot(browser, filename: str):
    """
    Takes a screenshot of the current browser page.
    This function is a skill that the agent can use.
    The 'browser' argument is passed by the agent automatically.
    """
    if not filename.endswith(".png"):
        filename += ".png"
    browser.screenshot(filename)
    return f"Screenshot saved as {filename}"

# This dictionary is used by the agent to discover the skills.
# The key is the command name, and the value is the function to execute.
SKILLS = {
    "SCREENSHOT": take_screenshot
} 