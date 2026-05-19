from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SPEEDTEST_URL = "https://www.speedtest.net/"
X_URL = "https://x.com/"
USER_EMAIL = "sample.com"
USERNAME = "Username"
PASSWORD = ""

options = Options()
options.add_experimental_option("detach", True)
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 200)

driver.get(SPEEDTEST_URL)

speedtest_button = driver.find_element(By.XPATH, value = "//span[text()='Go']")
speedtest_button.click()

download_speed = wait.until(
    lambda d: (
        (val := d.find_element(
            By.CSS_SELECTOR,
            value=".result-data-large.number.result-data-value.download-speed"
        ).text.strip())
        and val not in ("", "0", "—")
        and val
    ) or False
)

upload_speed = wait.until(
    lambda d: (
        (val := d.find_element(
            By.CSS_SELECTOR,
            value=".result-data-large.number.result-data-value.upload-speed"
        ).text.strip())
        and val not in ("", "0", "—")
        and val
    ) or False
)

float_download_speed = float(download_speed)
float_upload_speed = float(upload_speed)

# print(type(float_download_speed))
# print(upload_speed)

# if float_download_speed < 300 and float_upload_speed < 300:
    # driver.get(X_URL)
    #
    # sign_in_button = wait.until(
    #     EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign in']")
    #     )
    # )
    #
    # sign_in_button.click()
    #
    # email_input = wait.until(
    #     EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Phone, email, or username')]/following::input[1]")
    #                                    )
    # )
    #
    # email_input.send_keys(USER_EMAIL)
    #
    # next_button = driver.find_element(By.XPATH, value="//span[text()='Next']")
    # next_button.click()
    #
    # password_input = wait.until(
    #     EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Password')]/following::input[1]")
    #                                    )
    # )
    # password_input.send_keys(PASSWORD)
    #
    # login_button = driver.find_element(By.XPATH, value="//span[text()='Log in']")
    # login_button.click()
    #
    # x_text_box = wait.until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div')
    #                                    )
    # )
    # message = "Test"
    # x_text_box.send_keys(message)
    #
    # post_button = driver.find_element(By.XPATH, value="//span[text()='Post']")
    # post_button.click()