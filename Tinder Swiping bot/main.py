import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TINDER_URL = "https://tinder.com/"
BROWSER_PROFILE_DIRECTORY = r"--user-data-dir=C:\Users\Sunder\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default"
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

subprocess.Popen([
    BRAVE_PATH,
    "--remote-debugging-port=9222",
    f"--user-data-dir={BROWSER_PROFILE_DIRECTORY}"
])

options = Options()
options.debugger_address = "IP address"
driver = webdriver.Chrome(options=options)

driver.switch_to.new_window('tab')
driver.get(TINDER_URL)

wait = WebDriverWait(driver, 5)

swipe_left = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[.//span[text()='Nope']]")
    )
)

keep_swiping = True

while keep_swiping:
    swipe_left.click()