import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CommentScraper:
    def __init__(self, driver, post_link):
        """
        تهيئة الكائن بالمستعرض ورابط المنشور.
        Initialize the object with the web driver and post link.
        """
        self.driver = driver
        self.post_link = post_link
        self.wait = WebDriverWait(self.driver, 20)
        self.more_comments_attempts = 0
        self.posts_details = []
        self.raw_comments = []
        self.final_comments = []

    def fetch_post_details(self):
        """
        جلب تفاصيل المنشور مثل التسمية، عدد الإعجابات، ووقت النشر.
        Fetch post details such as caption, like count, and time posted.
        """
        self.driver.get(self.post_link)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)

        try:
            caption = self.wait.until(EC.presence_of_element_located((By.XPATH, "//article//ul/div[1]/li//h1")))
        except Exception as e:
            print(f"Error while fetching caption: {e}")  # Error while fetching caption
            caption = "NaN"

        try:
            count_of_like_element = self.driver.find_element(By.XPATH, "//article//section[2]//span/a/span/span")
            like_text = count_of_like_element.text.strip()
        except Exception as e:
            print(f"Error: {e}")  # Error: {e}
            like_text = "0"

        try:
            time_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//article//div[2]//div[2]//a/span/time"))
            )
            time_text = time_element.get_attribute("datetime")
            time_posted = time_text.split("T")[-1].split(".")[0]
            date_posted = time_text.split("T")[0]
        except Exception as e:
            print(f"Error: {e}")  # Error: {e}
            time_posted, date_posted = "NaN", "NaN"

        post_details = {
            "caption": caption.text,
            "count_of_likes": like_text,
            "post_url": self.post_link,
            "time_posted": time_posted,
            "date_posted": date_posted
        }
        self.posts_details.append(post_details)
        self.collect_raw_comments()

    def collect_raw_comments(self):
        """
        جمع التعليقات الخام من المنشور.
        Collect raw comments from the post.
        """
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        comments_table = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//article//ul/div[3]"))
        )

        while True:
            try:
                if self.more_comments_attempts == 1:
                    print("Stop collecting comments.")  # Stop collecting comments.
                    print("It has been verified that there are no other comments.")
                    print("\n---------------------------------------------------------------------------------------\n")
                    break

                self.raw_comments = comments_table.find_elements(By.CSS_SELECTOR, ".x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1yztbdb.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1")
                print(f"Current Length of Comments: {len(self.raw_comments)}")

                button_more_comments = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//section/main//article//ul/div[3]//li/div/button[@class='_abl-']"))
                )

                self.driver.execute_script("arguments[0].scrollIntoView(true);", button_more_comments)
                button_more_comments.click()
                time.sleep(2.5)

                new_comments = comments_table.find_elements(By.CSS_SELECTOR, ".x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1yztbdb.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1")

                if len(new_comments) > len(self.raw_comments):
                    self.more_comments_attempts = 0

            except Exception as e:
                self.more_comments_attempts += 1
                print("\n-------------------------------------------------------------------------------------------\n")
                print("Possibly, there are no further comments. We are checking...")



        self.process_and_store_comments()

    def process_and_store_comments(self):
        """
        معالجة وتخزين التعليقات المجمعة.
        Process and store the collected comments.
        """
        print("Data is being processed...")
        for index, comment in enumerate(self.raw_comments):

            try:
                commentor = comment.find_element(By.CSS_SELECTOR, "ul div li h3 a")
                commentor_name = commentor.text
                commentor_url = commentor.get_attribute("href")

                try:
                    comments = comment.find_element(By.CSS_SELECTOR, "._a9zs span._ap3a._aaco._aacu._aacx._aad7._aade")
                    comment_text = comments.text
                except Exception:
                    comment_text = "NaN"

                try:
                    replies = comment.find_element(By.XPATH, ".//button//span[@class='_a9yi']")
                    clean_replies = replies.text.split(" ")[-1].split("(")[-1].split(")")[0]
                except Exception:
                    clean_replies = "0"

                try:
                    likes = comment.find_element(By.XPATH, ".//span/button[1]/span")
                    likes_text = likes.text.strip().split(" ")[0]
                    likes_count = likes_text if likes_text.isdigit() else "0"
                except Exception:
                    likes_count = "0"

                try:
                    time_element = comment.find_element(By.XPATH, ".//a/time")
                    time_text = time_element.get_attribute("datetime")
                    time_posted = time_text.split("T")[-1].split(".")[0]
                    date_posted = time_text.split("T")[0]
                except Exception:
                    time_posted = "NaN"
                    date_posted = "NaN"

                # إنشاء قاموس التعليق
                # Creating the comment dictionary
                comment_data = {
                    "commentor_name": commentor_name,
                    "commentor_url": commentor_url,
                    "comment": comment_text,
                    "replies": clean_replies,
                    "likes": likes_count,
                    "time_posted": time_posted,
                    "date_posted": date_posted,
                }

                # إضافة التعليق إلى القائمة
                # Append the comment to the list
                self.final_comments.append(comment_data)

            except Exception as e:
                print(f"Error processing comment {index + 1}: {e}")

        print("Data appended successfully")
