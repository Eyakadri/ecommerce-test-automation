import pytest
from pages.login_page import LoginPage
from utils.config import Config


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.login
class TestLogin:
    """Test suite for login functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup for each test - initialize page object."""
        self.login_page = LoginPage(driver)
        self.login_page.navigate_to_login_page()
        yield   
    def test_valid_login_credentials(self, driver):
        """
        Test Case: Valid Login Credentials
        Steps:
            1. Navigate to login page
            2. Enter valid email
            3. Enter valid password
            4. Click Login button
        Expected:
            - User should be redirected to inventory page
            - Products should be visible
        """
        self.login_page.login(Config.TEST_USER_EMAIL, Config.TEST_USER_PASSWORD)
        
        assert self.login_page.is_login_successful(), "Login should be successful with valid credentials"
        assert self.login_page.is_inventory_displayed(), "Inventory should be visible after successful login"
    
    def test_login_with_wrong_password(self, driver):
        """
        Test Case: Login with Wrong Password
        Steps:
            1. Navigate to login page
            2. Enter valid email
            3. Enter wrong password
            4. Click Login button
        Expected:
            - Error message should be displayed
            - User should remain on login page
        """
        wrong_password = "wrongpassword123"
        self.login_page.login(Config.TEST_USER_EMAIL, wrong_password)
        
        assert self.login_page.is_error_displayed(), "Error message should be displayed for wrong password"
        assert "not match" in self.login_page.get_error_message().lower() or \
               "no match" in self.login_page.get_error_message().lower(), \
               "Error message should indicate password mismatch"
    
    def test_login_with_wrong_email(self, driver):
        """
        Test Case: Login with Wrong Email
        Steps:
            1. Navigate to login page
            2. Enter non-existent email
            3. Enter password
            4. Click Login button
        Expected:
            - Error message should be displayed
            - User should remain on login page
        """
        wrong_email = "nonexistent@example.com"
        self.login_page.login(wrong_email, Config.TEST_USER_PASSWORD)
        
        assert self.login_page.is_error_displayed(), "Error message should be displayed for wrong email"
        assert "not match" in self.login_page.get_error_message().lower() or \
               "do not match" in self.login_page.get_error_message().lower(), \
               "Error message should indicate credentials do not match"
    
    def test_login_with_empty_email(self, driver):
        """
        Test Case: Login with Empty Email
        Steps:
            1. Navigate to login page
            2. Leave email field empty
            3. Enter password
            4. Click Login button
        Expected:
            - Validation error for email field
            - Login should fail
        """
        self.login_page.enter_password(Config.TEST_USER_PASSWORD)
        self.login_page.click_login()
        
        assert self.login_page.is_error_displayed(), "Error message should be displayed for empty email"
    
    def test_login_with_empty_password(self, driver):
        """
        Test Case: Login with Empty Password
        Steps:
            1. Navigate to login page
            2. Enter email
            3. Leave password field empty
            4. Click Login button
        Expected:
            - Validation error for password field
            - Login should fail
        """
        self.login_page.enter_email(Config.TEST_USER_EMAIL)
        self.login_page.click_login()
        
        assert self.login_page.is_error_displayed(), "Error message should be displayed for empty password"
    
    def test_login_with_sql_injection_attempt(self, driver):
        """
        Test Case: SQL Injection Prevention in Email Field
        Steps:
            1. Navigate to login page
            2. Enter SQL injection payload in email field
            3. Enter password
            4. Click Login button
        Expected:
            - System should handle safely (no database error)
            - Error message or failed login (not exposed)
        """
        sql_injection_email = "test@example.com' OR '1'='1"
        self.login_page.login(sql_injection_email, Config.TEST_USER_PASSWORD)
        
        # Should either show error message or not login
        assert self.login_page.is_error_displayed() or not self.login_page.is_login_successful(), \
               "System should handle SQL injection safely"
