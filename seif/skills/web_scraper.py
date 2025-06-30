# seifcli/seif/skills/web_scraper.py

from rich.console import Console
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import os
import time

console = Console()

def extract_text(browser, selector: str, output_file: str = None):
    """
    Extracts text from elements matching the selector and optionally saves to a file.
    
    Args:
        browser: The browser instance
        selector: CSS selector to find elements
        output_file: Optional filename to save the extracted text
        
    Returns:
        A message indicating the result of the operation
    """
    if not browser.driver:
        return "Browser not initialized."
        
    console.print(f"Extracting text from elements matching [cyan]{selector}[/cyan]...")
    
    try:
        # Wait for elements to be present
        elements = WebDriverWait(browser.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
        
        if not elements:
            return f"No elements found matching selector: {selector}"
            
        # Extract text from all matching elements
        extracted_texts = [elem.text.strip() for elem in elements if elem.text.strip()]
        
        console.print(f"[green]✓[/green] Found {len(extracted_texts)} elements with text content")
        
        # Save to file if requested
        if output_file:
            if not output_file.endswith(".txt"):
                output_file += ".txt"
                
            with open(output_file, "w", encoding="utf-8") as f:
                for i, text in enumerate(extracted_texts):
                    f.write(f"Item {i+1}:\n{text}\n\n")
            
            return f"Extracted {len(extracted_texts)} text items and saved to {output_file}"
        else:
            # Display in console if not saving to file
            for i, text in enumerate(extracted_texts[:5]):
                console.print(f"[bold]Item {i+1}:[/bold]\n{text[:100]}..." if len(text) > 100 else f"[bold]Item {i+1}:[/bold]\n{text}")
                
            if len(extracted_texts) > 5:
                console.print(f"[dim]...and {len(extracted_texts) - 5} more items[/dim]")
                
            return f"Extracted {len(extracted_texts)} text items"
            
    except TimeoutException:
        return f"Timeout waiting for elements matching selector: {selector}"
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_links(browser, selector: str, output_file: str = None):
    """
    Extracts links (href attributes) from elements matching the selector.
    
    Args:
        browser: The browser instance
        selector: CSS selector to find link elements
        output_file: Optional filename to save the extracted links
        
    Returns:
        A message indicating the result of the operation
    """
    if not browser.driver:
        return "Browser not initialized."
        
    console.print(f"Extracting links from elements matching [cyan]{selector}[/cyan]...")
    
    try:
        # Wait for elements to be present
        elements = WebDriverWait(browser.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
        
        if not elements:
            return f"No elements found matching selector: {selector}"
            
        # Extract links and text from all matching elements
        extracted_links = []
        for elem in elements:
            href = elem.get_attribute("href")
            text = elem.text.strip()
            if href:
                extracted_links.append({"url": href, "text": text})
        
        console.print(f"[green]✓[/green] Found {len(extracted_links)} links")
        
        # Save to file if requested
        if output_file:
            if not output_file.endswith(".json"):
                output_file += ".json"
                
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(extracted_links, f, indent=2)
            
            return f"Extracted {len(extracted_links)} links and saved to {output_file}"
        else:
            # Display in console if not saving to file
            for i, link in enumerate(extracted_links[:5]):
                console.print(f"[bold]Link {i+1}:[/bold] {link['text']} - [cyan]{link['url']}[/cyan]")
                
            if len(extracted_links) > 5:
                console.print(f"[dim]...and {len(extracted_links) - 5} more links[/dim]")
                
            return f"Extracted {len(extracted_links)} links"
            
    except TimeoutException:
        return f"Timeout waiting for elements matching selector: {selector}"
    except Exception as e:
        return f"Error extracting links: {str(e)}"

# Export the skills
SKILLS = {
    "EXTRACT_TEXT": extract_text,
    "EXTRACT_LINKS": extract_links
}