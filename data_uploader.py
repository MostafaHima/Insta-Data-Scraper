import openpyxl
from datetime import date

class UploadData:
    """
    كلاس لتحميل بيانات الحساب والتعليقات إلى ملف Excel
    Class to upload account data and comments to an Excel file.
    """
    def __init__(self, comments, post_details, comment_counts, account_details):
        """
        تهيئة الكائن بالبيانات المطلوبة
        Initialize the object with required data.
        """
        self.comments = comments  # قائمة التعليقات لكل منشور
        self.post_details = post_details  # تفاصيل كل منشور
        self.comment_counts = comment_counts  # عدد التعليقات لكل منشور
        self.account_details = account_details  # تفاصيل الحساب
        self.workbook = openpyxl.Workbook()  # إنشاء ملف Excel جديد

    def upload_data_to_xlsx_file(self):
        """
        رفع البيانات إلى ملف Excel
        Upload the data to an Excel file.
        """
        # إنشاء الصفحة الرئيسية لمعلومات الحساب
        main_sheet = self.workbook.active
        main_sheet.title = "Account_Information"

        # إضافة رؤوس الأعمدة لمعلومات الحساب
        main_sheet.append(["Account Name", "Number of Posts", "Followers"])  # أسماء الأعمدة

        # إضافة بيانات الحساب
        for account in self.account_details:
            main_sheet.append([
                account.get("name", "NaN"),  # اسم الحساب
                account.get("count_of_posts", "NaN"),  # عدد المنشورات
                account.get("followers", "NaN")  # عدد المتابعين
            ])

        # إنشاء صفحات منفصلة لكل منشور
        for i, post_comments in enumerate(self.comments):
            # إنشاء صفحة جديدة لكل منشور
            post_sheet = self.workbook.create_sheet(title=f"Post {i + 1}")

            # إضافة تفاصيل المنشور
            for detail in self.post_details[i]:
                for key, value in detail.items():
                    post_sheet.append([key, value])

            # إضافة عدد التعليقات
            post_sheet.append(["Number of Comments", self.comment_counts[i]])

            # إضافة فراغ للفصل بين الأقسام
            post_sheet.append([])  # سطر فارغ
            post_sheet.append([])

            # إضافة رؤوس الأعمدة للتعليقات
            post_sheet.append([
                "Commentor Name", "Commentor URL", "Comment", "Replies", "Likes", "Time Posted", "Date Posted"
            ])

            # إضافة بيانات التعليقات
            for comment in post_comments:
                post_sheet.append([
                    comment.get("commentor_name", "NaN"),  # اسم المعلق
                    comment.get("commentor_url", "NaN"),  # رابط المعلق
                    comment.get("comment", "NaN"),  # نص التعليق
                    comment.get("replies", "NaN"),  # عدد الردود
                    comment.get("likes", "NaN"),  # عدد الإعجابات
                    comment.get("time_posted", "NaN"),  # الوقت
                    comment.get("date_posted", "NaN")  # التاريخ
                ])

        # حفظ الملف باسم مناسب يتضمن اسم الحساب وتاريخ اليوم
        file_name = f'{self.account_details[0]["name"]}_{date.today()}.xlsx'
        self.workbook.save(file_name)

        # طباعة رسالة تأكيد
        print("\n-------------------------------------------------------------------------------------------------\n")
        print(f"Data uploaded successfully to:[ {file_name} ]!")

