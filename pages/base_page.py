from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.config import Config
from utils.screenshot import ScreenshotManager


class BasePage:
    """
    Base class for all page objects.
    Handles common operations like waiting, element interactions, and screenshots.
    """
    
    def __init__(self, driver):
        """
        Initialize BasePage with WebDriver instance.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
    
    def navigate_to(self, url):
        """
        Navigate to a specific URL.
        
        Args:
            url: Full URL to navigate to
        """
        self.driver.get(url)
    
    def find_element(self, locator):
        """
        Find a single element using WebDriverWait.
        
        Args:
            locator: Tuple of (By.LOCATOR_TYPE, locator_string)
            
        Returns:
            WebElement if found
            
        Raises:
            TimeoutException if element not found within explicit wait
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            raise TimeoutException(f"Element not found: {locator}")
    
    def find_elements(self, locator):
        """
        Find multiple elements using WebDriverWait.
        
        Args:
            locator: Tuple of (By.LOCATOR_TYPE, locator_string)
            
        Returns:
            List of WebElements
        """
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            return []
    
    def click_element(self, locator):
        """
        Click an element after waiting for it to be clickable.
        
        Args:
            locator: Tuple of (By.LOCATOR_TYPE, locator_string)
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator, text):
        """
        Enter text into an input field.
        
        Args:
            locator: Tuple of (By.LOCATOR_TYPE, locator_string)
            text: Text to enter
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """
        Get text content from an element.
        
        Args:
            locator: Tuple of (By.LOCATOR_TYPE, locator_string)
            
        Returns:
            Text content of the element
        """
        element = self.find_element(locator)
        return element.text
    
    def get_attribute(self, locator, attribute_name):
        """
        Get an attribute value from an element.
        
        Args:
            locator: Tuple of (By.LOCATOR_TYPE, locator_string)
            attribute_name: Name of the attribute
            
        Returns:
            Attribute value
        """
        element = self.find_element(locator)
        return element.get_attribute(attribute_name)
    
    def is_element_visible(self, locator):
        """
        Check if an element is visible on the page.
        
        Args:
            locator: Tuple of (By.LOCATOR_TYPE, locator_string)
            
        Returns:
            True if visible, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator):
        """
        Check if an element is present in the DOM (not necessarily visible).
        
        Args:
            locator: Tuple of (By.LOCATOR_TYPE, locator_string)
            
        Returns:
            True if present, False otherwise
        """
        try:
            self.find_element(locator)
            return True
        except TimeoutException:
            return False
    
    def switch_to_frame(self, locator):
        """
        Switch to an iframe.
        
        Args:
            locator: Tuple of (By.LOCATOR_TYPE, locator_string)
        """
        frame = self.find_element(locator)
        self.driver.switch_to.frame(frame)
    
    def switch_to_default_content(self):
        """Switch back to main content from iframe."""
        self.driver.switch_to.default_content()
    
    def wait_for_url_change(self, original_url, timeout=None):
        """
        Wait for the URL to change from the original.
        
        Args:
            original_url: The original URL to compare against
            timeout: Custom timeout (uses explicit wait if not specified)
            
        Returns:
            True if URL changed
        """
        timeout = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(lambda driver: driver.current_url != original_url)
    
    def scroll_to_element(self, locator):
        """
        Scroll the page so an element is visible.
        
        Args:
            locator: Tuple of (By.LOCATOR_TYPE, locator_string)
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def take_screenshot(self, name="screenshot"):
        """
        Capture a screenshot of the current page.
        
        Args:
            name: Name for the screenshot file
            
        Returns:
            Path to the saved screenshot
        """
        return ScreenshotManager.take_screenshot(self.driver, name)
    
    def get_current_url(self):
        """
        Get the current page URL.
        
        Returns:
            Current URL string
        """
        return self.driver.current_url
    
    def get_page_title(self):
        """
        Get the current page title.
        
        Returns:
            Page title string
        """
        return self.driver.title
