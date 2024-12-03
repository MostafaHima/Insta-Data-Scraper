import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InstagramLogin:
    """
    Class to handle Instagram login and navigate to the account page.
    """

    def __init__(self, driver, email, password, account_search_url):
        """
        Initialize the class with login details and account information.
        """
        self.driver = driver  # WebDriver instance
        self.email = email  # Email or username for login
        self.password = password  # Password for login
        self.account_search_url = account_search_url  # URL of the target account
        self.wait = WebDriverWait(self.driver, 20)  # Maximum wait time of 20 seconds

    def login(self):
        """
        Log in to Instagram using email and password.
        """
        print("\n[INFO] Starting login process...")  # Log message indicating login start

        # Wait for the page to fully load
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        try:
            # Locate the username field
            print("[INFO] Locating username field...")
            username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_field.send_keys(self.email)  # Enter the email or username

            # Locate the password field
            print("[INFO] Locating password field...")
            password_field = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_field.send_keys(self.password, Keys.ENTER)  # Enter the password and press Enter

            time.sleep(5)  # Wait for login to complete
            print("[SUCCESS] Login completed successfully!")  # Success message
        except Exception as e:
            print(f"[ERROR] Login failed: {e}")  # Error message with exception details

    def navigate_to_account(self):
        """
        Navigate to the specified account page.
        """
        print("\n[INFO] Navigating to the account page...")  # Log message indicating navigation start
        try:
            time.sleep(10)  # Brief delay to avoid being flagged by Instagram
            self.driver.get(self.account_search_url)  # Load the target account page
            print("[SUCCESS] Successfully loaded the account page!")  # Success message
        except Exception as e:
            print(f"[ERROR] Failed to navigate to account page: {e}")  # Error message with exception details

        print("\n---------------------------------------------------------------\n")
