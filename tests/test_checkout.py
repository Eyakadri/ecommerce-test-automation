import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.config import Config


def js_click(driver, element):
    driver.execute_script("arguments[0].click();", element)


def js_fill(driver, field_id, value):
    driver.execute_script("""
        var input = document.getElementById(arguments[0]);
        var setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value').set;
        setter.call(input, arguments[1]);
        input.dispatchEvent(new Event('input', { bubbles: true }));
    """, field_id, value)


def go_to_cart(driver):
    cart_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_link"))
    )
    js_click(driver, cart_link)
    WebDriverWait(driver, 10).until(EC.url_contains("cart"))


def go_to_checkout(driver):
    checkout_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "checkout"))
    )
    js_click(driver, checkout_btn)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "first-name"))
    )


def fill_form(driver, first, last, postal):
    for field_id, value in [
        ("first-name", first),
        ("last-name", last),
        ("postal-code", postal)
    ]:
        js_fill(driver, field_id, value)
    time.sleep(0.3)


def submit_form(driver):
    continue_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "continue"))
    )
    js_click(driver, continue_btn)
    WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-two"))


def finish_order(driver):
    finish_btn = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "finish"))
    )
    time.sleep(0.5)
    js_click(driver, finish_btn)
    WebDriverWait(driver, 15).until(EC.url_contains("checkout-complete"))


@pytest.mark.regression
@pytest.mark.checkout
class TestCheckout:
    """Test suite for checkout functionality on SauceDemo."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Login and add item to cart before each checkout test."""
        self.cart_page = CartPage(driver)
        self.checkout_page = CheckoutPage(driver)

        driver.get(Config.BASE_URL)
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_container"))
        )

        add_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-test='add-to-cart-sauce-labs-backpack']")
            )
        )
        add_btn.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[data-test='remove-sauce-labs-backpack']")
            )
        )
        yield

    def test_guest_checkout_happy_path(self, driver):
        """Full checkout flow: cart → info → overview → complete."""
        go_to_cart(driver)
        go_to_checkout(driver)
        fill_form(driver, "John", "Doe", "12345")
        submit_form(driver)
        finish_order(driver)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='checkout-complete-container'], .checkout_complete_container"))
        )
        assert self.checkout_page.is_order_complete(), \
            "Order complete page should be displayed"

    def test_checkout_order_complete_message(self, driver):
        """Order complete page should show thank you message."""
        go_to_cart(driver)
        go_to_checkout(driver)
        fill_form(driver, "Jane", "Smith", "54321")
        submit_form(driver)
        finish_order(driver)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='checkout-complete-container'], .checkout_complete_container"))
        )
        message = self.checkout_page.get_order_complete_message()
        assert message and len(message) > 0, \
            "Order complete message should be displayed"

    def test_checkout_empty_first_name_shows_error(self, driver):
        """Submitting checkout form without first name should show error."""
        self.cart_page.navigate_to_cart()
        self.checkout_page.navigate_to_checkout()
        self.checkout_page.enter_last_name("Doe")
        self.checkout_page.enter_postcode("12345")
        self.checkout_page.click_continue()
        assert self.checkout_page.is_error_displayed(), \
            "Error should be displayed when first name is missing"

    def test_checkout_empty_last_name_shows_error(self, driver):
        """Submitting checkout form without last name should show error."""
        self.cart_page.navigate_to_cart()
        self.checkout_page.navigate_to_checkout()
        self.checkout_page.enter_first_name("John")
        self.checkout_page.enter_postcode("12345")
        self.checkout_page.click_continue()
        assert self.checkout_page.is_error_displayed(), \
            "Error should be displayed when last name is missing"

    def test_checkout_empty_postcode_shows_error(self, driver):
        """Submitting checkout form without postcode should show error."""
        self.cart_page.navigate_to_cart()
        self.checkout_page.navigate_to_checkout()
        self.checkout_page.enter_first_name("John")
        self.checkout_page.enter_last_name("Doe")
        self.checkout_page.click_continue()
        assert self.checkout_page.is_error_displayed(), \
            "Error should be displayed when postcode is missing"

    def test_checkout_order_summary_shows_item(self, driver):
        """Overview page should show the item added to cart."""
        go_to_cart(driver)
        go_to_checkout(driver)
        fill_form(driver, "John", "Doe", "12345")
        submit_form(driver)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )
        items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(items) > 0, "Order summary should display at least one item"
