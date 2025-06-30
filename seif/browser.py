# seifcli/seif/browser.py - Enhanced Version

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from rich.console import Console
from rich.prompt import Prompt
from selenium_stealth import stealth
import time
import random
from typing import Dict, Optional, List
from urllib.parse import urlparse

console = Console()

class Browser:
    def __init__(self, config: Dict = None):
        """Enhanced browser initialization with configuration."""
        self.config = config or {}
        self.driver = None
        self.current_page_info = {}
        self._initialize_driver()

    def _initialize_driver(self):
        """Initialize the Selenium WebDriver with enhanced options."""
        try:
            options = Options()
            
            # Configure based on config
            if self.config.get("headless", False):
                options.add_argument("--headless")
            
            # Window size
            window_size = self.config.get("window_size", "1920,1080")
            options.add_argument(f"--window-size={window_size}")
            
            # Enhanced stealth options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # User agent
            user_agent = self.config.get("user_agent", 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36")
            options.add_argument(f"user-agent={user_agent}")
            
            with console.status("[bold blue]Starting enhanced browser...", spinner="earth"):
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                
                # Apply stealth settings
                stealth(driver,
                        languages=["en-US", "en"],
                        vendor="Google Inc.",
                        platform="Win32",
                        webgl_vendor="Intel Inc.",
                        renderer="Intel Iris OpenGL Engine",
                        fix_hairline=True,
                        )
                
                # Remove automation indicators
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                self.driver = driver
                self.wait = WebDriverWait(driver, self.config.get("timeout", 10))

            console.print("[bold green]Enhanced browser started successfully.[/bold green]")
            
        except Exception as e:
            console.print(f"[bold red]Error initializing browser: {e}[/bold red]")
            self.driver = None

    def _update_page_info(self):
        """Update information about the current page."""
        if not self.driver:
            return
            
        try:
            self.current_page_info = {
                "url": self.driver.current_url,
                "title": self.driver.title,
                "domain": urlparse(self.driver.current_url).netloc,
                "timestamp": time.time()
            }
        except Exception:
            pass

    def _get_element_info(self, element) -> Dict:
        """Get detailed information about an element."""
        try:
            return {
                "tag": element.tag_name,
                "text": element.text[:100],  # Truncate long text
                "attributes": {
                    "id": element.get_attribute("id"),
                    "class": element.get_attribute("class"),
                    "name": element.get_attribute("name"),
                    "type": element.get_attribute("type")
                },
                "location": element.location,
                "size": element.size,
                "visible": element.is_displayed(),
                "enabled": element.is_enabled()
            }
        except Exception:
            return {}

    def goto(self, url: str) -> Optional[str]:
        """Navigate to URL with enhanced error handling."""
        if not self.driver:
            return "Browser not initialized."
            
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        console.print(f"Navigating to [cyan]{url}[/cyan]...")
        
        try:
            self.driver.get(url)
            time.sleep(random.uniform(1, 3))  # Random delay to appear human
            self._update_page_info()
            
            # Wait for page to load
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            
            console.print(f"[green]Successfully loaded: {self.driver.title}[/green]")
            return None
            
        except TimeoutException:
            return f"Timeout loading {url}"
        except WebDriverException as e:
            return f"Failed to navigate to {url}: {e.msg}"
        except Exception as e:
            return f"Unexpected error navigating to {url}: {str(e)}"

    def find_elements_smart(self, selector: str) -> List:
        """Smart element finding with multiple strategies."""
        if not self.driver:
            return []
            
        strategies = [
            (By.CSS_SELECTOR, selector),
            (By.XPATH, f"//*[@id='{selector}']"),
            (By.NAME, selector),
            (By.CLASS_NAME, selector),
            (By.XPATH, f"//*[contains(@placeholder, '{selector}')]"),
            (By.XPATH, f"//*[contains(@aria-label, '{selector}')]"),
            (By.XPATH, f"//*[contains(text(), '{selector}')]")
        ]
        
        for by, value in strategies:
            try:
                elements = self.driver.find_elements(by, value)
                if elements:
                    return elements
            except Exception:
                continue
                
        return []

    def type(self, selector: str, text: str) -> Optional[str]:
        """Enhanced typing with multiple fallback strategies."""
        if not self.driver:
            return "Browser not initialized."

        console.print(f"Typing '{text[:50]}{'...' if len(text) > 50 else ''}' into element...")

        # Domain-specific optimizations
        domain = self.current_page_info.get("domain", "")
        
        # Strategy 1: Smart element finding
        elements = self.find_elements_smart(selector)
        
        if not elements:
            # Strategy 2: Wait for element to appear
            try:
                element = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                elements = [element]
            except TimeoutException:
                pass
        
        # Strategy 3: Try common input selectors
        if not elements:
            common_selectors = [
                "input[type='text']", "input[type='search']", "textarea",
                "input[name='q']", "input[name='search']", "#search", ".search-input"
            ]
            
            for sel in common_selectors:
                elements = self.find_elements_smart(sel)
                if elements:
                    break
        
        if not elements:
            return f"Could not find element with selector: {selector}"
        
        # Use the first visible and enabled element
        target_element = None
        for element in elements:
            try:
                if element.is_displayed() and element.is_enabled():
                    target_element = element
                    break
            except Exception:
                continue
        
        if not target_element:
            return "No suitable input element found"
        
        try:
            # Enhanced typing strategy
            element_info = self._get_element_info(target_element)
            console.print(f"[dim]Found {element_info.get('tag', 'element')} element[/dim]")
            
            # Clear existing content
            target_element.clear()
            time.sleep(random.uniform(0.1, 0.3))
            
            # Focus the element
            target_element.click()
            time.sleep(random.uniform(0.1, 0.3))
            
            # Type with human-like behavior
            for char in text:
                target_element.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            # Trigger input event for modern web apps
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", 
                target_element
            )
            
            console.print("[green]✅ Text typed successfully[/green]")
            return None
            
        except Exception as e:
            return f"Error typing text: {str(e)}"

    def click(self, selector: str) -> Optional[str]:
        """Enhanced clicking with multiple strategies."""
        if not self.driver:
            return "Browser not initialized."
            
        console.print(f"Clicking element: {selector}")
        
        # Find elements using smart strategy
        elements = self.find_elements_smart(selector)
        
        # Domain-specific optimizations
        domain = self.current_page_info.get("domain", "")
        if "google.com" in domain:
            google_selectors = [
                "input[name='btnK']", "button[type='submit']", 
                "input[type='submit']", "button[jsname='VlcLAe']"
            ]
            for sel in google_selectors:
                google_elements = self.find_elements_smart(sel)
                if google_elements:
                    elements.extend(google_elements)
        
        if not elements:
            return f"Could not find clickable element: {selector}"
        
        # Find the best element to click
        target_element = None
        for element in elements:
            try:
                if element.is_displayed() and element.is_enabled():
                    target_element = element
                    break
            except Exception:
                continue
        
        if not target_element:
            return "No clickable element found"
        
        try:
            # Multiple click strategies
            element_info = self._get_element_info(target_element)
            console.print(f"[dim]Clicking {element_info.get('tag', 'element')}[/dim]")
            
            # Strategy 1: Scroll to element and click
            self.driver.execute_script("arguments[0].scrollIntoView(true);", target_element)
            time.sleep(random.uniform(0.5, 1.0))
            
            # Strategy 2: Try ActionChains for more human-like clicking
            try:
                ActionChains(self.driver).move_to_element(target_element).click().perform()
                console.print("[green]✅ Clicked using ActionChains[/green]")
                return None
            except Exception:
                pass
            
            # Strategy 3: Direct click
            try:
                target_element.click()
                console.print("[green]✅ Clicked directly[/green]")
                return None
            except Exception:
                pass
            
            # Strategy 4: JavaScript click
            self.driver.execute_script("arguments[0].click();", target_element)
            console.print("[green]✅ Clicked using JavaScript[/green]")
            return None
            
        except Exception as e:
            return f"Error clicking element: {str(e)}"

    def scroll(self, direction: str, amount: int = None) -> Optional[str]:
        """Enhanced scrolling with configurable amount."""
        if not self.driver:
            return "Browser not initialized."
            
        if amount is None:
            amount = 500 if direction in ["down", "up"] else 0
            
        console.print(f"Scrolling {direction}...")
        
        try:
            if direction == "down":
                self.driver.execute_script(f"window.scrollBy(0, {amount});")
            elif direction == "up":
                self.driver.execute_script(f"window.scrollBy(0, -{amount});")
            elif direction == "top":
                self.driver.execute_script("window.scrollTo(0, 0);")
            elif direction == "bottom":
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            else:
                return f"Unknown scroll direction: {direction}"
                
            time.sleep(random.uniform(0.5, 1.0))
            return None
            
        except Exception as e:
            return f"Error scrolling: {str(e)}"

    def screenshot(self, filename: str) -> Optional[str]:
        """Enhanced screenshot with automatic filename handling."""
        if not self.driver:
            return "Browser not initialized."
            
        if not filename.endswith(('.png', '.jpg', '.jpeg')):
            filename += '.png'
            
        console.print(f"Taking screenshot: [cyan]{filename}[/cyan]")
        
        try:
            self.driver.save_screenshot(filename)
            console.print(f"[green]Screenshot saved: {filename}[/green]")
            return None
        except Exception as e:
            return f"Failed to take screenshot: {str(e)}"

    def get_page_source(self) -> str:
        """Get the current page source."""
        if not self.driver:
            return ""
        return self.driver.page_source

    def get_current_url(self) -> str:
        """Get the current URL."""
        if not self.driver:
            return ""
        return self.driver.current_url

    def wait_for_element(self, selector: str, timeout: int = 10):
        """Wait for an element to be present."""
        if not self.driver:
            return None
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
        except TimeoutException:
            return None

    def close(self):
        """Close the browser with cleanup."""
        if self.driver:
            try:
                console.print("[bold blue]Closing browser...[/bold blue]")
                self.driver.quit()
                console.print("[green]Browser closed successfully[/green]")
            except Exception as e:
                console.print(f"[yellow]Warning: Error closing browser: {e}[/yellow]")
            finally:
                self.driver = None