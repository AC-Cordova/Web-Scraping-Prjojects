import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_experimental_option("detach", True)
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 5)

driver.get("https://ozh.github.io/cookieclicker/")

en_lang = wait.until(
    EC.element_to_be_clickable((By.ID, 'langSelect-EN'))
)
en_lang.click()

last_upgrade_check = time.time()
while True:

    cookie = wait.until(
        EC.element_to_be_clickable((By.ID, 'bigCookie'))
    )
    cookie.click()

    if time.time() - last_upgrade_check >= 60*5:

        cookie_data = driver.find_element(By.ID, value='cookies')
        cookie_count = cookie_data.text
        cookie_int = int(cookie_count.split()[0])

        products = driver.find_elements(By.CSS_SELECTOR, value='#products .product')

        highest_price = 0
        best_product = None

        for product in products:
            price_element = product.find_element(By.CSS_SELECTOR, value='span.price')
            text = price_element.text.strip()

            if text == "":
                continue

            price_int = int(text.replace(",", ""))

            if highest_price < price_int <= cookie_int:
                highest_price = price_int
                best_product = product

        if best_product:
            best_product.click()

        last_upgrade_check = time.time()

# print(highest_price)
# print(cookie_int)
# print(best_product.text)
