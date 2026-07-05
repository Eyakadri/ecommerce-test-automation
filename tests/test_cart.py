import pytest
from selenium.webdriver.common.by import By
from pages.cart_page import CartPage
from pages.product_page import ProductPage
from utils.config import Config


@pytest.mark.regression
@pytest.mark.cart
class TestCart:
    """Test suite for shopping cart functionality on SauceDemo."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Login and prepare for each cart test."""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        self.driver = driver
        self.cart_page = CartPage(driver)
        self.product_page = ProductPage(driver)
        driver.get(Config.BASE_URL)
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        # Wait until inventory page is loaded before proceeding
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_container"))
        )
        yield

    def test_add_single_item_to_cart(self, driver):
        driver.find_element(
            By.CSS_SELECTOR, "button[data-test='add-to-cart-sauce-labs-backpack']"
        ).click()
        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert badge.text == "1", "Cart badge should show 1 after adding one item"

    def test_add_multiple_items_to_cart(self, driver):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Click first product
        first_add = driver.find_element(
            By.CSS_SELECTOR, "button[data-test='add-to-cart-sauce-labs-backpack']"
        )
        driver.execute_script("arguments[0].click();", first_add)

        # Wait for first button to become "Remove" before clicking second
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[data-test='remove-sauce-labs-backpack']")
            )
        )

        # Now click second product
        second_add = driver.find_element(
            By.CSS_SELECTOR, "button[data-test='add-to-cart-sauce-labs-bike-light']"
        )
        driver.execute_script("arguments[0].click();", second_add)

        # Wait for second button to become "Remove"
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[data-test='remove-sauce-labs-bike-light']")
            )
        )

        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert badge.text == "2", "Cart badge should show 2 after adding two items"
        self.cart_page.navigate_to_cart()
        count = self.cart_page.get_cart_items_count()
        assert count == 2, f"Cart should have 2 items, found {count}"

    def test_remove_item_from_cart(self, driver):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        driver.find_element(
            By.CSS_SELECTOR, "button[data-test='add-to-cart-sauce-labs-backpack']"
        ).click()

        # Wait for item to be added
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[data-test='remove-sauce-labs-backpack']")
            )
        )

        self.cart_page.navigate_to_cart()
        count_before = self.cart_page.get_cart_items_count()
        assert count_before == 1, "Cart should have 1 item before removal"
        self.cart_page.remove_product_from_cart(0)
        count_after = self.cart_page.get_cart_items_count()
        assert count_after == 0, "Cart should be empty after removing the item"

    def test_empty_cart_state(self, driver):
        self.cart_page.navigate_to_cart()
        count = self.cart_page.get_cart_items_count()
        assert count == 0, "Cart should be empty when nothing was added"
        continue_btn = driver.find_element(By.ID, "continue-shopping")
        assert continue_btn.is_displayed(), \
            "Continue shopping button should be visible on empty cart"

    def test_cart_persists_after_navigation(self, driver):
        driver.find_element(
            By.CSS_SELECTOR, "button[data-test='add-to-cart-sauce-labs-backpack']"
        ).click()
        driver.get(Config.BASE_URL + "/inventory.html")
        self.cart_page.navigate_to_cart()
        count = self.cart_page.get_cart_items_count()
        assert count == 1, "Cart item should persist after navigating away"

    def test_cart_badge_updates_with_each_item(self, driver):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        products = [
            ("add-to-cart-sauce-labs-backpack",  "remove-sauce-labs-backpack"),
            ("add-to-cart-sauce-labs-bike-light", "remove-sauce-labs-bike-light"),
            ("add-to-cart-sauce-labs-bolt-t-shirt", "remove-sauce-labs-bolt-t-shirt"),
        ]

        for i, (add_id, remove_id) in enumerate(products):
            add_button = driver.find_element(
                By.CSS_SELECTOR, f"button[data-test='{add_id}']"
            )
            driver.execute_script("arguments[0].click();", add_button)
            # Wait for button to flip to Remove before checking badge
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"button[data-test='{remove_id}']")
                )
            )
            badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            assert badge.text == str(i + 1), \
                f"Badge should show {i + 1} after adding {i + 1} items"
