import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Centralized configuration management using environment variables."""
    
    # Browser Configuration
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    
    # Application URL
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    
    # Test Credentials
    TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "test@example.com")
    TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "password123")
    
    # Timeouts (in seconds)
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "15"))
    
    # Screenshot Settings
    TAKE_SCREENSHOT_ON_FAILURE = os.getenv("TAKE_SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    SCREENSHOT_PATH = os.getenv("SCREENSHOT_PATH", "screenshots/")
    
    # Report Settings
    REPORT_PATH = os.getenv("REPORT_PATH", "reports/")
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist."""
        for directory in [cls.SCREENSHOT_PATH, cls.REPORT_PATH]:
            os.makedirs(directory, exist_ok=True)
