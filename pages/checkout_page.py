from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import Config


class CheckoutPage(BasePage):
    """Page Object for SauceDemo Checkout page."""
    
    # Locators for SauceDemo checkout
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    ORDER_COMPLETE_CONTAINER = (By.CSS_SELECTOR, "[data-test='checkout-complete-container'], .checkout_complete_container")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message-container")
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CHECKOUT_COMPLETE_TEXT = (By.CSS_SELECTOR, "[data-test='complete-text'], .complete-text")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.page_url = f"{Config.BASE_URL}/checkout-step-one.html"
    
    def navigate_to_checkout(self):
        """Navigate to checkout page."""
        self.navigate_to(self.page_url)
        return self
    
    def enter_first_name(self, first_name):
        """Enter first name using JavaScript for React compatibility."""
        self.driver.execute_script("""
            var input = document.getElementById('first-name');
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(input, arguments[0]);
            input.dispatchEvent(new Event('input', { bubbles: true }));
        """, first_name)
        return self

    def enter_last_name(self, last_name):
        """Enter last name using JavaScript for React compatibility."""
        self.driver.execute_script("""
            var input = document.getElementById('last-name');
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(input, arguments[0]);
            input.dispatchEvent(new Event('input', { bubbles: true }));
        """, last_name)
        return self

    def enter_postcode(self, postcode):
        """Enter postal code using JavaScript for React compatibility."""
        self.driver.execute_script("""
            var input = document.getElementById('postal-code');
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(input, arguments[0]);
            input.dispatchEvent(new Event('input', { bubbles: true }));
        """, postcode)
        return self
    
    def fill_checkout_info(self, first_name, last_name, postcode):
        """
        Fill the complete checkout form.
        
        Args:
            first_name: First name
            last_name: Last name
            postcode: Postal code
        """
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postcode(postcode)
        return self
    
    def click_continue(self):
        """Click Continue button using JavaScript."""
        btn = self.find_element(self.CONTINUE_BUTTON)
        self.driver.execute_script("arguments[0].click();", btn)
        return self
    
    def click_finish(self):
        """Click Finish button to complete order."""
        self.click_element(self.FINISH_BUTTON)
        return self
    
    def is_order_complete(self):
        """
        Check if order is complete.
        
        Returns:
            True if complete container is visible
        """
        return self.is_element_visible(self.ORDER_COMPLETE_CONTAINER)
    
    def get_order_complete_message(self):
        """Get the order completion message."""
        if self.is_element_visible(self.CHECKOUT_COMPLETE_TEXT):
            return self.get_text(self.CHECKOUT_COMPLETE_TEXT)
        return None
    
    def is_error_displayed(self):
        """Check if error message is displayed."""
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def get_error_message(self):
        """Get error message text."""
        if self.is_error_displayed():
            return self.get_text(self.ERROR_MESSAGE)
        return None

        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_address(address)
        self.enter_city(city)
        self.enter_postcode(postcode)
        return self
    
    def click_continue_billing(self):
        """Click Continue button on billing section."""
        self.click_element(self.CONTINUE_BILLING_BUTTON)
        return self
    
    def click_continue_shipping_address(self):
        """Click Continue button on shipping address section."""
        self.click_element(self.CONTINUE_SHIPPING_BUTTON)
        return self
    
    def click_continue_shipping_method(self):
        """Click Continue button on shipping method section."""
        self.click_element(self.CONTINUE_SHIPPING_METHOD)
        return self
    
    def click_continue_payment_method(self):
        """Click Continue button on payment method section."""
        self.click_element(self.CONTINUE_PAYMENT_METHOD)
        return self
    
    def confirm_order(self):
        """Click the Confirm Order button."""
        self.click_element(self.CONFIRM_ORDER_BUTTON)
        return self
    
    def is_order_confirmation_displayed(self):
        """
        Check if order confirmation page is displayed.
        
        Returns:
            True if success message visible
        """
        return self.is_element_visible(self.ORDER_SUCCESS_MESSAGE)
    
    def get_order_confirmation_message(self):
        """Get the order confirmation message."""
        if self.is_order_confirmation_displayed():
            return self.get_text(self.ORDER_SUCCESS_MESSAGE)
        return None
    
    def get_order_id(self):
        """Get the order ID from confirmation page."""
        if self.is_order_confirmation_displayed():
            return self.get_text(self.ORDER_ID)
        return None
    
    def get_order_summary(self):
        """
        Get order summary with products.
        
        Returns:
            Dictionary with order details
        """
        return {
            'total': self.get_text(self.ORDER_TOTAL),
            'confirmation': self.is_order_confirmation_displayed()
        }
    
    def is_postcode_error_displayed(self):
        """Check if postcode validation error is displayed."""
        # Would check for specific error message near postcode field
        return False  # Placeholder
    
    def is_required_field_error_displayed(self):
        """Check if any required field error is displayed."""
        try:
            # Check for validation error messages
            errors = self.find_elements((By.CSS_SELECTOR, ".error"))
            return len(errors) > 0
        except:
            return False
