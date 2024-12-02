"""
Script Overview:
This script automates the process of scraping Instagram account data. It logs into the account, collects account details,
post URLs, and comments, and then uploads the collected data into an Excel file.

Author: Mostafa Ibrahim Ahmed

Instructions:
Please make sure to update your Instagram login credentials and input the target Instagram URL.
"""

import time
from selenium import webdriver
from login_manager import InstagramLogin
from account_info_scraper import AccountDetails
from post_urls_scraper import PostsLink
from comments_scraper import CommentScraper
from data_uploader import UploadData

# Variables to store collected data
all_comments = []  # List to store all comments collected from posts
all_details = []  # List to store all post details
counts_comments = []  # List to store the count of comments per post

# Instagram profile URL
"https://www.instagram.com/yasmine_sabri/"

# User login credentials - Update with your own credentials
email = "mostafabr185@gmail.com"
password = "36XY/2g3PSZ,HD?"

# Chrome options for running the script
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # Keep the browser open after execution

# Input the target Instagram URL
orignal_url = input("Enter the Instagram URL: ")
prepre_url = orignal_url.split("/")  # Split URL to extract domain
new_url = f"{prepre_url[0]}//{prepre_url[2]}"  # Format URL for correct navigation

# Initialize the WebDriver (Chrome browser) and navigate to the target URL
driver = webdriver.Chrome(options=chrome_options)
driver.get(url=new_url)

# Initialize Instagram login and perform login process
init_login = InstagramLogin(driver=driver, email=email, password=password, account_search_url=orignal_url)
init_login.login()  # Login to Instagram
init_login.navigate_to_account()  # Navigate to the account page

# Wait for page to load and collect account details
time.sleep(7)
init_account_details = AccountDetails(driver=driver)
account_details = init_account_details.get_account_details()

# Collect the URLs of posts from the profile
init_posts_link = PostsLink(driver=driver)
links = init_posts_link.collection_post_url()  # Get post URLs

# Iterate over each post URL to collect details and comments
print("\n-----------------------------------------------------------------------------------------------------------")
for index, link in enumerate(links, start=1):
    print(f"Processing Post: {index}\n")

    # Initialize comment scraper and collect comments for the post
    init_collection_comments = CommentScraper(driver=driver, post_link=link)
    collection_comments = init_collection_comments.fetch_post_details()  # Fetch post details and comments

    # Store the collected data for each post
    all_comments.append(init_collection_comments.final_comments)
    all_details.append(init_collection_comments.posts_details)
    counts_comments.append(len(init_collection_comments.final_comments))  # Count comments per post

    print(f"Finished Post: {index}")
    print("\n=======================================================================================================\n")
    time.sleep(5)  # Wait before processing the next post


# Upload the collected data to an Excel file
upload = UploadData(comments=all_comments, post_details=all_details, comment_counts=counts_comments, account_details=account_details)
upload.upload_data_to_xlsx_file()  # Upload the data

print("Data collection and upload complete!")
print("\n-------------------------------------------------------------------------------------------------------------")