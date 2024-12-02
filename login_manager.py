import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InstagramLogin:
    """
    كلاس لتسجيل الدخول إلى إنستغرام والوصول إلى صفحة الحساب
    Class to handle Instagram login and navigate to the account page.
    """

    def __init__(self, driver, email, password, account_search_url):
        """
        تهيئة الكلاس ببيانات تسجيل الدخول ومعلومات الحساب
        Initialize the class with login details and account information.
        """
        self.driver = driver
        self.email = email
        self.password = password
        self.account_search_url = account_search_url
        self.wait = WebDriverWait(self.driver, 20)  # حد الانتظار الأقصى 20 ثانية

    def login(self):
        """
        تسجيل الدخول باستخدام البريد الإلكتروني وكلمة المرور.
        Login to Instagram using email and password.
        """
        print("\n[INFO] Starting login process...")  # عرض رسالة بداية العملية

        # انتظار تحميل الصفحة الرئيسية
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        try:
            # العثور على حقل اسم المستخدم
            print("[INFO] Locating username field...")
            username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_field.send_keys(self.email)

            # العثور على حقل كلمة المرور
            print("[INFO] Locating password field...")
            password_field = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_field.send_keys(self.password, Keys.ENTER)

            time.sleep(5)  # انتظار التأكيد بعد الإرسال
            print("[SUCCESS] Login completed successfully!")  # رسالة نجاح
        except Exception as e:
            print(f"[ERROR] Login failed: {e}")

    def navigate_to_account(self):
        """
        الانتقال إلى صفحة الحساب المطلوب.
        Navigate to the specified account page.
        """
        print("\n[INFO] Navigating to the account page...")
        try:
            time.sleep(10)  # انتظار قليل لتجنب الحظر
            self.driver.get(self.account_search_url)
            print("[SUCCESS] Successfully loaded the account page!")
        except Exception as e:
            print(f"[ERROR] Failed to navigate to account page: {e}")

        print("\n---------------------------------------------------------------\n")




