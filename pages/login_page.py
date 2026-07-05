from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import Config


class LoginPage(BasePage):
    """Page Object for SauceDemo Login page."""
    
    # Locators as class variables (SauceDemo)
    EMAIL_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    INVENTORY_CONTAINER = (By.CLASS_NAME, "inventory_container")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.page_url = f"{Config.BASE_URL}/"
    
    def navigate_to_login_page(self):
        """Navigate to the login page."""
        self.navigate_to(self.page_url)
        return self
    
    def enter_email(self, email):
        """Enter username in the username field."""
        self.enter_text(self.EMAIL_INPUT, email)
        return self
    
    def enter_password(self, password):
        """Enter password in the password field."""
        self.enter_text(self.PASSWORD_INPUT, password)
        return self
    
    def click_login(self):
        """Click the Login button."""
        self.click_element(self.LOGIN_BUTTON)
        return self
    
    def login(self, email, password):
        """
        Perform login action with username and password.
        
        Args:
            email: User username
            password: User password
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return self
    
    def get_error_message(self):
        """
        Get error message text if login failed.
        
        Returns:
            Error message text or None if not visible
        """
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def is_error_displayed(self):
        """
        Check if error message is displayed.
        
        Returns:
            True if error message is visible
        """
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def is_login_successful(self):
        """
        Verify if login was successful by checking for inventory container.
        
        Returns:
            True if logged in (inventory page visible)
        """
        return self.is_element_visible(self.INVENTORY_CONTAINER)
    
    def is_inventory_displayed(self):
        """
        Check if inventory/products are displayed (indicates successful login).
        
        Returns:
            True if inventory container is visible
        """
        return self.is_element_visible(self.INVENTORY_CONTAINER)
