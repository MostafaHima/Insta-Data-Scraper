from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class PostsLink:
    """
    كلاس لجمع روابط المنشورات من صفحة إنستغرام.
    Class for collecting post URLs from an Instagram page.
    """
    def __init__(self, driver):
        """
        تهيئة الكائن بالمستعرض.
        Initialize the object with the web driver.
        """
        self.driver = driver  # مستعرض الويب
        self.clean_links = set()  # مجموعة لتخزين الروابط الفريدة
        self.scroll_attempts = 0  # عداد لمحاولات التمرير

    def collection_post_url(self):
        """
        جمع روابط المنشورات باستخدام التمرير في الصفحة.
        Collect post URLs by scrolling through the page.
        """
        try:
            # الانتظار حتى يظهر عنصر المنشورات الرئيسي
            div_posts = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//section/main/div/div[2]/div"))
            )

            print("Starting to collect post URLs...")
            print("\n----------------------------------------------------------------------------------\n")

            while True:
                try:
                    # عدد الروابط قبل التمرير
                    previous_count = len(self.clean_links)

                    # العثور على جميع الروابط الجديدة
                    links = div_posts.find_elements(By.CSS_SELECTOR, "div a")
                    for link in links:
                        self.clean_links.add(link.get_attribute('href'))

                    # عدد الروابط بعد التمرير
                    current_count = len(self.clean_links)
                    print(f"Number of links collected so far: {current_count}")

                    # التحقق إذا تم جمع 12 رابطًا (عدد منشورات محدود)
                    if current_count >= 12:
                        print("Collected enough links. Exiting...")
                        break

                    # التحقق من زيادة عدد الروابط
                    if current_count > previous_count:
                        self.scroll_attempts = 0  # إعادة تعيين المحاولات إذا تم العثور على روابط جديدة
                    else:
                        self.scroll_attempts += 1
                        print(f"Scroll attempts without new links: {self.scroll_attempts}")

                    # تمرير الصفحة تدريجيًا
                    for _ in range(4):  # تمرير الصفحة تدريجيًا 4 خطوات
                        self.driver.execute_script("window.scrollBy(0, 500);")
                        time.sleep(2)

                    # التوقف عند الوصول إلى الحد الأقصى للمحاولات
                    if self.scroll_attempts > 5:
                        print("No more new links loaded. Exiting...")
                        break

                except Exception as e:
                    print(f"An error occurred during scrolling: {e}")
                    break

        except Exception as e:
            print(f"An error occurred during initialization: {e}")

        return self.clean_links
