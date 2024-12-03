from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AccountDetails:
    """
    Class to fetch Instagram account details.
    """
    def __init__(self, driver):
        """
        Initialize the object with the web driver and maximum wait time.
        """
        self.driver = driver  # Web driver instance
        self.wait = WebDriverWait(self.driver, 30)  # Maximum wait time of 30 seconds
        self.account_details = []  # List to store account details

    def get_account_details(self):
        """
        Fetch account details: account name, post count, and followers.
        """
        # Wait until the page is fully loaded
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Fetch the account name
        account_name = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//header/section[2]//h2/span"))
        )

        # Fetch the post count
        post_count = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//header/section[3]//span/span"))
        )

        # Fetch the follower count
        followers_count = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//header/section[3]//li[2]//span/span"))
        )

        # Store account details in a dictionary
        account_info = {
            "name": account_name.text,  # Account name
            "count_of_posts": post_count.text,  # Number of posts
            "followers": followers_count.text  # Number of followers
        }

        # Add the details to the list
        self.account_details.append(account_info)

        # Return the account details
        return self.account_details



