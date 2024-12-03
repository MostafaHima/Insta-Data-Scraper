from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class PostsLink:
    """
    A class to collect Instagram post URLs from a user or hashtag page by scrolling.
    """

    def __init__(self, driver):
        """
        Initialize the object with the provided web driver.

        Parameters:
        - driver: Selenium WebDriver instance for browser interaction.
        """
        self.driver = driver  # Selenium WebDriver instance.
        self.clean_links = set()  # Set to store unique post URLs.
        self.scroll_attempts = 0  # Counter for tracking consecutive scrolls without finding new links.

    def collection_post_url(self):
        """
        Collects Instagram post URLs by scrolling the page.

        Returns:
        - A set of unique URLs representing the posts collected from the page.
        """
        try:
            # Wait for the main posts container to load.
            div_posts = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//section/main/div/div[2]/div"))
            )

            print("Starting to collect post URLs...")
            print("\n----------------------------------------------------------------------------------\n")

            while True:
                try:
                    # Save the count of links collected before scrolling.
                    previous_count = len(self.clean_links)

                    # Find all anchor tags inside the posts container and add their href attributes to the set.
                    links = div_posts.find_elements(By.CSS_SELECTOR, "div a")
                    for link in links:
                        self.clean_links.add(link.get_attribute('href'))

                    # Save the count of links collected after scrolling.
                    current_count = len(self.clean_links)
                    print(f"Number of links collected so far: {current_count}")

                    # Stop collecting once 12 links are gathered (assuming a limit per requirement).
                    if current_count >= 12:
                        print("Collected enough links. Exiting...")
                        break

                    # If new links were found, reset scroll attempts.
                    if current_count > previous_count:
                        self.scroll_attempts = 0
                    else:
                        # Increment the scroll attempts if no new links are found.
                        self.scroll_attempts += 1
                        print(f"Scroll attempts without new links: {self.scroll_attempts}")

                    # Scroll the page down in increments to load more content.
                    for _ in range(4):  # Perform four small scrolls for gradual loading.
                        self.driver.execute_script("window.scrollBy(0, 500);")
                        time.sleep(2)

                    # Exit the loop if the maximum number of scroll attempts is reached.
                    if self.scroll_attempts > 5:
                        print("No more new links loaded. Exiting...")
                        break

                except Exception as e:
                    print(f"An error occurred during scrolling: {e}")
                    break

        except Exception as e:
            print(f"An error occurred during initialization: {e}")

        return self.clean_links
