from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import Config


class ProductPage(BasePage):
    """Page Object for SauceDemo Product detail page."""
    
    # Locators for SauceDemo
    PRODUCT_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name'], .inventory_details_name_large")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "[data-test='inventory-item-price'], .inventory_details_price")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, "[data-test='inventory-item-image'], .inventory_details_img")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, "[data-test='inventory-item-desc'], .inventory_details_desc")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "[data-test='add-to-cart'], #add-to-cart")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "[data-test='remove'], #remove")
    BACK_TO_PRODUCTS = (By.CSS_SELECTOR, "[data-test='back-to-products'], #back-to-products")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_product_name(self):
        """
        Get the product name.
        
        Returns:
            Product name text
        """
        return self.get_text(self.PRODUCT_NAME)
    
    def get_product_price(self):
        """
        Get the product price.
        
        Returns:
            Product price text
        """
        return self.get_text(self.PRODUCT_PRICE)
    
    def is_product_price_displayed(self):
        """
        Check if product price is displayed.
        
        Returns:
            True if price is visible
        """
        return self.is_element_visible(self.PRODUCT_PRICE)
    
    def is_product_name_displayed(self):
        """
        Check if product name is displayed.
        
        Returns:
            True if product name is visible
        """
        return self.is_element_visible(self.PRODUCT_NAME)
    
    def is_product_description_displayed(self):
        """
        Check if product description is displayed.
        
        Returns:
            True if description is visible
        """
        return self.is_element_visible(self.PRODUCT_DESCRIPTION)
    
    def get_product_description(self):
        """Get the product description text."""
        if self.is_product_description_displayed():
            return self.get_text(self.PRODUCT_DESCRIPTION)
        return None
    
    def add_to_cart(self):
        """Click 'Add to Cart' button using JavaScript for React compatibility."""
        button = self.find_element(self.ADD_TO_CART_BUTTON)
        self.driver.execute_script("arguments[0].click();", button)
        return self
    
    def remove_from_cart(self):
        """Click 'Remove' button (if product is in cart) using JavaScript."""
        if self.is_element_visible(self.REMOVE_BUTTON):
            button = self.find_element(self.REMOVE_BUTTON)
            self.driver.execute_script("arguments[0].click();", button)
        return self
    
    def back_to_products(self):
        """Click 'Back' button to return to products list."""
        self.click_element(self.BACK_TO_PRODUCTS)
        return self
    
    def is_add_to_cart_button_displayed(self):
        """
        Check if 'Add to Cart' button is displayed.
        
        Returns:
            True if button is visible
        """
        return self.is_element_visible(self.ADD_TO_CART_BUTTON)
    
    def is_remove_button_displayed(self):
        """
        Check if 'Remove' button is displayed (product is in cart).
        
        Returns:
            True if remove button is visible
        """
        return self.is_element_visible(self.REMOVE_BUTTON)

