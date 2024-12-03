import openpyxl
from datetime import date

class UploadData:
    """
    Class to upload account data and comments to an Excel file.
    """
    def __init__(self, comments, post_details, comment_counts, account_details):
        """
        Initialize the object with required data.
        """
        self.comments = comments  # List of comments for each post
        self.post_details = post_details  # Details of each post
        self.comment_counts = comment_counts  # Number of comments per post
        self.account_details = account_details  # Account details
        self.workbook = openpyxl.Workbook()  # Create a new Excel workbook

    def upload_data_to_xlsx_file(self):
        """
        Upload the data to an Excel file.
        """
        # Create the main sheet for account information
        main_sheet = self.workbook.active
        main_sheet.title = "Account_Information"

        # Add column headers for account information
        main_sheet.append(["Account Name", "Number of Posts", "Followers"])  # Column headers

        # Add account data
        for account in self.account_details:
            main_sheet.append([
                account.get("name", "NaN"),  # Account name
                account.get("count_of_posts", "NaN"),  # Number of posts
                account.get("followers", "NaN")  # Number of followers
            ])

        # Create separate sheets for each post
        for i, post_comments in enumerate(self.comments):
            # Create a new sheet for each post
            post_sheet = self.workbook.create_sheet(title=f"Post {i + 1}")

            # Add post details
            for detail in self.post_details[i]:
                for key, value in detail.items():
                    post_sheet.append([key, value])  # Key-value pairs for post details

            # Add the number of comments
            post_sheet.append(["Number of Comments", self.comment_counts[i]])

            # Add empty rows to separate sections
            post_sheet.append([])  # Empty row
            post_sheet.append([])

            # Add column headers for comments
            post_sheet.append([
                "Commentor Name", "Commentor URL", "Comment", "Replies", "Likes", "Time Posted", "Date Posted"
            ])

            # Add comment data
            for comment in post_comments:
                post_sheet.append([
                    comment.get("commentor_name", "NaN"),  # Commentor's name
                    comment.get("commentor_url", "NaN"),  # Commentor's profile URL
                    comment.get("comment", "NaN"),  # Comment text
                    comment.get("replies", "NaN"),  # Number of replies
                    comment.get("likes", "NaN"),  # Number of likes
                    comment.get("time_posted", "NaN"),  # Time the comment was posted
                    comment.get("date_posted", "NaN")  # Date the comment was posted
                ])

        # Save the file with a name that includes the account name and today's date
        file_name = f'{self.account_details[0]["name"]}_{date.today()}.xlsx'
        self.workbook.save(file_name)

        # Print confirmation message
        print("\n-------------------------------------------------------------------------------------------------\n")
        print(f"Data uploaded successfully to: [ {file_name} ]!")
