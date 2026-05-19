from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

IG_URL = "https://instagram.com/"
TONY_URL = "https://www.instagram.com/Sample/"
USER_NAME = "Sample"
PASSWORD = "Sample"

options = Options()
options.add_experimental_option("detach", True)
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

driver = webdriver.Chrome(options=options)
driver.get(IG_URL)

username_input = driver.find_element(By.NAME, value = "email")
username_input.send_keys(USER_NAME)

password_input = driver.find_element(By.NAME, value="pass")
password_input.send_keys(PASSWORD)

login_button = driver.find_element(By.XPATH, value="//span[text()='Log in']")
login_button.click()

wait = WebDriverWait(driver, 5)

time.sleep(30)
driver.get(TONY_URL)

followers_button = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//a[contains(@href, '/followers')]")
    )
)

followers_button.click()

followers_box = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[@role='dialog']")
    )
)

#Get follower names(for testing)
# users = wait.until(EC.presence_of_all_elements_located(
#     (By.XPATH, "//div[@role='dialog']//a[contains(@href, '/')]")
# ))
#
# followers = []
# for user in users:
#     follower = user.text
#     followers.append(follower)
#
# print(followers)
#

#Click on follow buttons
# follow_buttons = wait.until(
#     EC.presence_of_all_elements_located(
#         (By.XPATH, "//button[.//div[text()='Follow']]")
#     )
# )
#
# for button in follow_buttons:
#     button.click()