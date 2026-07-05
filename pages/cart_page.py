from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import Config


class CartPage(BasePage):
    """Page Object for SauceDemo Shopping Cart page."""
    
    # Locators for SauceDemo
    CART_LINK = (By.ID, "shopping_cart_container")
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[data-test^='remove']")
    EMPTY_CART_MESSAGE = (By.CLASS_NAME, "cart_empty_cont")
    CART_SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    CART_TOTAL = (By.CLASS_NAME, "summary_total_label")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.page_url = f"{Config.BASE_URL}/cart.html"
    
    def navigate_to_cart(self):
        """Navigate to shopping cart page."""
        self.navigate_to(self.page_url)
        return self
    
    def get_cart_items_count(self):
        """
        Get the number of items in cart.
        
        Returns:
            Number of cart items
        """
        items = self.find_elements(self.CART_ITEMS)
        return len(items)
    
    def is_cart_empty(self):
        """
        Check if cart is empty.
        
        Returns:
            True if empty message is displayed
        """
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)
    
    def get_empty_cart_message(self):
        """Get the empty cart message text."""
        if self.is_cart_empty():
            return self.get_text(self.EMPTY_CART_MESSAGE)
        return None
    
    def is_cart_items_visible(self):
        """
        Check if cart items are visible.
        
        Returns:
            True if items are displayed
        """
        return self.get_cart_items_count() > 0
    
    def get_product_names_in_cart(self):
        """
        Get all product names in cart.
        
        Returns:
            List of product names
        """
        items = self.find_elements(self.CART_ITEMS)
        names = []
        for item in items:
            try:
                name = item.find_element(*self.PRODUCT_NAME).text
                names.append(name)
            except:
                pass
        return names
    
    def remove_product_from_cart(self, product_index=0):
        """
        Remove a product from cart by index.

        Args:
            product_index: Index of the product to remove (0-based)
        """
        remove_btns = self.find_elements(self.REMOVE_BUTTON)
        if product_index < len(remove_btns):
            self.driver.execute_script("arguments[0].click();", remove_btns[product_index])
        return self
    
    def get_cart_subtotal(self):
        """
        Get the cart subtotal.
        
        Returns:
            Subtotal text
        """
        if self.is_element_visible(self.CART_SUBTOTAL):
            return self.get_text(self.CART_SUBTOTAL)
        return None
    
    def get_cart_total(self):
        """
        Get the cart total.
        
        Returns:
            Total price text
        """
        if self.is_element_visible(self.CART_TOTAL):
            return self.get_text(self.CART_TOTAL)
        return None
    
    def proceed_to_checkout(self):
        """Click the Checkout button."""
        self.click_element(self.CHECKOUT_BUTTON)
        return self
    
    def continue_shopping(self):
        """Click Continue Shopping button."""
        if self.is_element_visible(self.CONTINUE_SHOPPING_BUTTON):
            self.click_element(self.CONTINUE_SHOPPING_BUTTON)
        return self

    def wait_for_cart_badge(self, expected_count):
        """Wait until cart badge shows expected count."""
        from selenium.webdriver.support import expected_conditions as EC
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "shopping_cart_badge"), str(expected_count)
            )
        )
