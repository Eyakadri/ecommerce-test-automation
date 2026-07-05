import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.config import Config
from utils.screenshot import ScreenshotManager


@pytest.fixture(scope="function")
def driver():
    Config.ensure_directories()

    if Config.BROWSER == "chrome":
        options = webdriver.ChromeOptions()
        if Config.HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--window-size=1920,1080")

        driver_manager = ChromeDriverManager()
        driver_path = driver_manager.install()

        if os.path.isdir(driver_path):
            driver_dir = driver_path
        else:
            driver_dir = os.path.dirname(driver_path)

        chromedriver_bin = None
        for fname in os.listdir(driver_dir):
            full = os.path.join(driver_dir, fname)
            try:
                if fname.startswith('chromedriver') and os.path.isfile(full):
                    chromedriver_bin = full
                    break
            except Exception:
                continue

        if not chromedriver_bin:
            for fname in os.listdir(driver_dir):
                full = os.path.join(driver_dir, fname)
                try:
                    if not os.path.isfile(full):
                        continue
                    with open(full, 'rb') as fh:
                        header = fh.read(4)
                        if header.startswith(b"\x7fELF"):
                            chromedriver_bin = full
                            break
                except Exception:
                    continue

        if not chromedriver_bin:
            raise RuntimeError(f"Could not locate chromedriver binary in {driver_dir}")

        os.chmod(chromedriver_bin, 0o755)
        service = Service(chromedriver_bin)
        driver = webdriver.Chrome(service=service, options=options)

    elif Config.BROWSER == "firefox":
        options = webdriver.FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {Config.BROWSER}")

    yield driver
    driver.quit()


@pytest.fixture(scope="function", autouse=True)
def take_screenshot_on_failure(request, driver):
    yield

    failed = False
    if getattr(getattr(request.node, "rep_setup", None), "failed", False):
        failed = True
    elif getattr(getattr(request.node, "rep_call", None), "failed", False):
        failed = True

    if failed:
        try:
            test_name = request.node.name
            ScreenshotManager.take_screenshot_on_failure(driver, test_name)
        except Exception:
            pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: Quick sanity check tests")
    config.addinivalue_line("markers", "regression: Full regression suite")
    config.addinivalue_line("markers", "login: Login functionality tests")
    config.addinivalue_line("markers", "register: Registration functionality tests")
    config.addinivalue_line("markers", "search: Search functionality tests")
    config.addinivalue_line("markers", "product: Product page functionality tests")
    config.addinivalue_line("markers", "cart: Shopping cart functionality tests")
    config.addinivalue_line("markers", "checkout: Checkout functionality tests")
