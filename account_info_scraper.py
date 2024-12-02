from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AccountDetails:
    """
    كلاس لجلب تفاصيل حساب الإنستغرام
    Class to fetch Instagram account details.
    """
    def __init__(self, driver):
        """
        تهيئة الكائن بالمستعرض ومهلة الانتظار.
        Initialize the object with the driver and wait time.
        """
        self.driver = driver  # مستعرض الويب
        self.wait = WebDriverWait(self.driver, 50)  # مدة الانتظار القصوى
        self.account_details = []  # قائمة لتخزين تفاصيل الحساب

    def get_account_details(self):
        """
        جلب تفاصيل الحساب (الاسم، عدد المنشورات، وعدد المتابعين).
        Fetch account details (name, post count, and followers).
        """
        # الانتظار حتى يتم تحميل الصفحة
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # جلب اسم الحساب
        account_name = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//header/section[2]//h2/span"))
        )

        # جلب عدد المنشورات
        post_count = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//header/section[3]//span/span"))
        )

        # جلب عدد المتابعين
        followers_count = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//header/section[3]//li[2]//span/span"))
        )

        # تجميع تفاصيل الحساب في شكل قاموس
        account_info = {
            "name": account_name.text,  # اسم الحساب
            "count_of_posts": post_count.text,  # عدد المنشورات
            "followers": followers_count.text  # عدد المتابعين
        }

        # إضافة التفاصيل إلى القائمة
        self.account_details.append(account_info)

        # إعادة التفاصيل
        return self.account_details






