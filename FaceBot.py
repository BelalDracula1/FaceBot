from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

class FaceBot:
    def __init__(self,username = None, password = None):
        self.username = username
        self.password = password
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")
        options.add_argument("--lang=en-US")
        self.browser = webdriver.Chrome(executable_path="chromedriver.exe",options=options)
    
    def login(self,chain = True):
        if chain:
            if self.browser.current_url != "https://facebook.com/login/?next=https://www.facebook.com/home.php":
                self.browser.get("https://facebook.com/login/?next=https://www.facebook.com/home.php")
        else:
            self.browser.get("https://facebook.com/login/?next=https://www.facebook.com/home.php")
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(self.username)
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.ID, "pass"))).send_keys(self.password)
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.ID, "loginbutton"))).click()
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH,"//a[@aria-label='Home']")))

    def logout(self):
        self.browser.delete_all_cookies()
        self.browser.execute_script('window.localStorage.clear();')
        self.browser.execute_script('window.sessionStorage.clear();')
        self.browser.get("https://facebook.com/login/?next=https://www.facebook.com/home.php")
    
    def follow(self,page_link):
        self.browser.get(page_link)
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='See Options']")))
        self.browser.execute_script("""document.querySelector("div[aria-label='See Options']").click()""")
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Follow']"))).click()

    def like(self,post_link,like_type,chain = True):
        if chain:
            if self.browser.current_url != post_link:
                self.browser.get(post_link)
        else:
           self.browser.get(post_link)
        like_types = {
            1: "//div[@aria-label='Love']",
            2: "//div[@aria-label='Care']",
            3: "//div[@aria-label='Haha']",
            4: "//div[@aria-label='Wow']",
            5: "//div[@aria-label='Sad']",
            6: "//div[@aria-label='Angry']"
        }
        like_btn = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Like']")))
        if like_type == 0:
            like_btn.click()
            return
        action = ActionChains(self.browser)
        action.move_to_element(like_btn).perform()
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, like_types[like_type]))).click()

    def comment(self,post_link,comment,chain = True):
        if chain:
            if self.browser.current_url != post_link:
                self.browser.get(post_link)
        else:
           self.browser.get(post_link)
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Leave a comment']"))).click()
        comment_input = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Write a comment']")))
        comment_input.send_keys(comment)
        comment_input.send_keys(Keys.ENTER)
    
    def share(self,post_link,chain = True):
        if chain:
            if self.browser.current_url != post_link:
                self.browser.get(post_link)
        else:
           self.browser.get(post_link) 
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Send this to friends or post it on your timeline.']"))).click()
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Share now')]"))).click()

    def joinGroup(self,group_link):
        self.browser.get(group_link)
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Join group']"))).click()

    def lockProfile(self):
        self.browser.get("https://facebook.com/profile")
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='See Options']")))
        self.browser.execute_script("""document.querySelector("div[aria-label='See Options']").click()""")
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Lock profile']"))).click()
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Lock Your Profile']"))).click()

    def close(self):
        self.browser.close()

    def config(self,username = None,password = None):
        if username:
            self.username = username
        if password:
            self.password = password

    def __exit__(self):
        self.close()
