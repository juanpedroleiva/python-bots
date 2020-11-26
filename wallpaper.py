from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
import requests

# Options to configure
options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')




class WallpaperBot:
    

    def wait(self, path, type_use):
        if type_use == "id":
            WebDriverWait(self.driver, 60).until(
                lambda x: x.find_element_by_id(path))
        if type_use == "xpath":
            WebDriverWait(self.driver, 60).until(
                lambda x: x.find_element_by_xpath(path))

    def __init__(self, amount):
        for i in range(amount):
            self.driver = webdriver.Chrome(options=options)

            # Go to Random Section with parameters
            self.driver.get("https://wallhaven.cc/search?categories=100&purity=100&atleast=2560x1440&sorting=random&order=desc")
            
            # Select first preview
            self.wait("//a[@class='preview']", "xpath")
            self.driver.find_element_by_xpath("//a[@class='preview']")\
                .click()
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.wait("//*[@id='wallpaper']", "xpath")

            # Download the image and manipulates the title
            src = str(self.driver.find_element_by_xpath("//*[@id='wallpaper']").get_attribute('src'))
            alt = str(self.driver.find_element_by_xpath("//*[@id='wallpaper']").get_attribute('alt')).split(' ')
            title = alt[1:10]
            title = "_".join(title)
            print(title)
        
            img_data = requests.get(src).content
            with open(title+'.png', 'wb') as handler:
                handler.write(img_data)

            self.driver.quit()





Bot = WallpaperBot(2)
