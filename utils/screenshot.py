import os
import re
from datetime import datetime
from utils.config import Config


class ScreenshotManager:
    """Handles screenshot capture and file management."""

    @staticmethod
    def take_screenshot(driver, test_name):
        """
        Capture a screenshot and save it with timestamp.

        Args:
            driver: Selenium WebDriver instance
            test_name: Name of the test for filename

        Returns:
            Path to the saved screenshot file
        """
        Config.ensure_directories()

        safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", test_name).strip("_") or "screenshot"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{safe_name}_{timestamp}.png"
        filepath = os.path.join(Config.SCREENSHOT_PATH, filename)

        try:
            if not hasattr(driver, "save_screenshot"):
                raise RuntimeError("Driver does not support screenshot capture")

            result = driver.save_screenshot(filepath)
            if result is False:
                raise RuntimeError("save_screenshot returned False")

            print(f"✓ Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"✗ Failed to save screenshot: {str(e)}")
            return None

    @staticmethod
    def take_screenshot_on_failure(driver, test_name):
        """
        Conditionally take screenshot based on config setting.

        Args:
            driver: Selenium WebDriver instance
            test_name: Name of the test for filename
        """
        if Config.TAKE_SCREENSHOT_ON_FAILURE:
            return ScreenshotManager.take_screenshot(driver, f"FAILED_{test_name}")
        return None
