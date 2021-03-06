"""
This is a bot built in Selenium that counts and lists every user from
the "Following" and "Followers" tab from the account it's being accessed.

This bot is also built with a self-correcting mechanism that recounts the
users if, for some reason (i.e. server lagging) the count was wrong, according
to the number presented on the user's profile.

"""
import sys
from time import sleep
from selenium import webdriver
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

class InstaBot:
    """This is the main class used in this bot
    It takes in the username and password of the account to be analysed 
    and returns the list of Followers, Following users and the "Unfollowers", 
    which is how people that the user follows but they don't follow back are
    later referenced.
    """

    def __init__(self, username, pw):
        '''Initial setup and login of the user's account, and dismissing popups.'''

        self.driver = webdriver.Chrome(chrome_options=options)
        self.username = username

        # Enter url and wait for page to load and maxes out the window
        self.driver.get("https://www.instagram.com/")
        sleep(2)
        self.driver.maximize_window()

        # Log in details and submit
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(4)

        # Dismiss popups
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button')\
            .click()
        sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')\
            .click()
        sleep(2)

    def get_unfollowers(self):

        # Flow control variables.
        isWorkingFollowers = 1
        isWorkingFollowing = 1

        # Counts the iterations the bot went through.
        iter_following = 1
        iter_followers = 1

        # If the either the amount Followers or the Following counted is different than what is shown on profile, repeat.
        while isWorkingFollowers == 1 or isWorkingFollowing == 1:

            # Go to user's profile or refreshes the page in case the website freezes.
            sleep(2)
            self.driver.get("https://www.instagram.com/")
            sleep(3)

            self.driver.find_element_by_xpath(f"//a[contains(@href,'/{self.username}')]")\
                .click()
            sleep(2)

            if isWorkingFollowing == 1:
                print(f"Counting Following users. Attempts: {iter_following}.")

                # Find and click "Following"
                all_elements = self.driver.find_elements_by_xpath("//span[@class=\"g47SY \"]")
                num_following = all_elements[2].text
                num_following = int(num_following.replace(".",""))
                print(f"The amount of people following should be equal to: {num_following}.")
                self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()

                # Get names function and stops the loop if the Count is correct.
                following = self.get_names()
                if num_following == len(following):
                    isWorkingFollowing = 0

                # Print list of following the user has
                print(f"Total following counted: {len(following)}.")
                if isWorkingFollowing == 1:
                    print("Encountered a problem when counting following users, recounting...") 
                    iter_following += 1                   
                else:
                    print(f"Following counting complete! Done in {iter_following} attempts.")
                    # print(following)

            if isWorkingFollowers == 1: 
                print(f"Counting Followers. Attempts: {iter_followers}.")

                # Find and click "Followers"
                all_elements = self.driver.find_elements_by_xpath("//span[@class=\"g47SY \"]")
                num_followers = all_elements[1].text
                num_followers = int(num_followers.replace(".",""))
                print(f"The amount of followers should be equal to: {num_followers}")
                self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
                    .click()
            
                # Get names function and stops the loop if the Count is correct.
                followers = self.get_names()
                if num_followers == len(followers):
                    isWorkingFollowers = 0
                
                # Print list of followers the user has
                print(f"Total followers counted: {len(followers)}.")
                if isWorkingFollowers == 1:
                    print("Encountered a problem when counting followers, recounting...") 
                    iter_followers += 1                   
                else:
                    print(f"Follower counting complete! Done in {iter_followers} attempts.")
                    # print(followers)

        # Creates list of users that don't follow back
        not_following_back = [user for user in following if user not in followers]

        # Print unfollowers list
        print("List of unfollowers generated succesfully.")
        print(f"Total (un)followers: {len(not_following_back)}.")
        print(not_following_back)

    def get_names(self):
        '''This is the function that retrieves the accounts' usernames in either following or followers tab.'''

        # Wait for the page to load
        sleep(2)

        # Find scrollbox
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

        # Scrolls the scrollbar until the end and saves the usernames in a list
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(0.5)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        sleep(1)

        # Close button
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button')\
            .click()
        return names

# Future GUI implemantation.
def window():
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("Test")

    win.show()
    sys.exit(app.exec_())


user = 'Insert username'
password = 'Insert password'

bot = InstaBot(user, password)
bot.get_unfollowers()
