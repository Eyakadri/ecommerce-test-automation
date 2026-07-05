import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.config import Config


@pytest.mark.regression
@pytest.mark.product
class TestProduct:
    """Test suite for product page functionality on SauceDemo."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Login, then navigate to a product detail page."""
        self.product_page = ProductPage(driver)
        self.cart_page = CartPage(driver)

        # Login
        driver.get(Config.BASE_URL)
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # Wait for inventory page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='inventory-container'], .inventory_container"))
        )

        # Navigate directly to product page — avoids WSL2 click timing issue
        driver.get(Config.BASE_URL + "/inventory-item.html?id=4")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='inventory-item-name'], .inventory_details_name_large"))
        )
        yield

    def test_product_name_displayed(self, driver):
        """Product name should be visible and not empty."""
        assert self.product_page.is_product_name_displayed(), \
            "Product name should be displayed"
        name = self.product_page.get_product_name()
        assert name and len(name) > 0, "Product name should not be empty"

    def test_product_price_displayed(self, driver):
        """Product price should be visible and not empty."""
        assert self.product_page.is_product_price_displayed(), \
            "Product price should be displayed"
        price = self.product_page.get_product_price()
        assert price and len(price) > 0, "Product price should not be empty"
        assert "$" in price, "Price should contain dollar sign"

    def test_product_description_displayed(self, driver):
        """Product description should be visible and not empty."""
        assert self.product_page.is_product_description_displayed(), \
            "Product description should be displayed"
        desc = self.product_page.get_product_description()
        assert desc and len(desc) > 0, "Product description should not be empty"

    def test_add_to_cart_button_displayed(self, driver):
        """Add to cart button should be visible before adding."""
        assert self.product_page.is_add_to_cart_button_displayed(), \
            "Add to cart button should be visible"

    def test_add_to_cart_updates_counter(self, driver):
        """Adding product should update cart badge to 1."""
        self.product_page.add_to_cart()
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert badge.text == "1", "Cart badge should show 1 after adding product"

    def test_add_to_cart_shows_remove_button(self, driver):
        """After adding to cart, Remove button should appear."""
        self.product_page.add_to_cart()
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='remove'], #remove"))
        )
        assert self.product_page.is_remove_button_displayed(), \
            "Remove button should appear after adding to cart"

    def test_remove_from_cart_shows_add_button(self, driver):
        """After removing from cart, Add to cart button should reappear."""
        self.product_page.add_to_cart()
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='remove'], #remove"))
        )
        self.product_page.remove_from_cart()
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='add-to-cart'], #add-to-cart"))
        )
        assert self.product_page.is_add_to_cart_button_displayed(), \
            "Add to cart button should reappear after removing"
