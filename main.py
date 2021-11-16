from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from send_email import send_email
from dotenv import load_dotenv
import os
import time

load_dotenv("./.env")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")

CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"
SUBREDDIT_URL = "https://old.reddit.com/r/Calgary/"
PHONY_URL = "https://old.reddit.com/r/MMA/"


class RedditBot:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.posts = None
        self.users = None
        self.message = ""

    def get_posts(self):
        self.driver.get(SUBREDDIT_URL)
        time.sleep(5)
        username_input = self.driver.find_element_by_name("user")
        username_input.send_keys(USERNAME)
        password_input = self.driver.find_element_by_name("passwd")
        password_input.send_keys(PASSWORD)
        login_button = self.driver.find_element_by_css_selector(".submit .btn")
        login_button.click()
        time.sleep(5)

        try:
            careers_thread = self.driver.find_element_by_link_text("Weekly Career/Employment Advice & Discussion Thread")
            careers_thread_link = careers_thread.get_attribute("href")
            careers_thread.click()
        except NoSuchElementException:
            # if no careers thread found, send email indicating no thread was found this week.
            self.message += "Sorry, no thread was found this week! Check back next week!"
        else:
            time.sleep(5)
            post_count = 0
            # list of posts and users from non-collapsed divs (posts that haven't been downvoted and hidden)
            self.posts = self.driver.find_elements_by_css_selector(".nestedlisting .noncollapsed .usertext .usertext-body")
            self.users = self.driver.find_elements_by_css_selector(".nestedlisting .noncollapsed .author")
            self.message += f"Here are the posts this week from the weekly career/employment advice & discussion thread in /r/Calgary ({careers_thread_link}):"
            for post in self.posts:
                user = self.users[post_count]
                post_count += 1
                self.message += f"<br><br>{post_count}. {user.text} posted: '{post.text}'"
        finally:
            time.sleep(5)
            send_email(self.message)
            self.driver.quit()


bot = RedditBot()
bot.get_posts()