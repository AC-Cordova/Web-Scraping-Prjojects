from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ZILLOW_CLONE_LINK = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSdg0WH0IqtED3tCSpCgkQX-W_SlKNqk5FL1-Qsv9eNGyfgVrA/viewform"

response = requests.get(ZILLOW_CLONE_LINK)
zillow_webpage = response.text

soup = BeautifulSoup(zillow_webpage, "html.parser")

property_cards = soup.find_all(name="div", class_="StyledPropertyCardDataWrapper")
links_list = []

for card in property_cards:
    link = card.select_one('a[data-test="property-card-link"]')
    links_list.append(link['href'])

ap_address = soup.select('address[data-test="property-card-addr"]')
address_list = [
    addr.get_text(strip=True).split("|")[-1].strip()
    for addr in ap_address
]

ap_price = soup.select('span[data-test="property-card-price"]')
price_list = [
    price.get_text() for price in ap_price
]

print(address_list)
print(price_list)
print(links_list)

options = Options()
options.add_experimental_option("detach", True)
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

driver = webdriver.Chrome(options=options)
driver.get(GOOGLE_FORM_LINK)

wait = WebDriverWait(driver, 5)

for address, price, link in zip(address_list, price_list, links_list):

    input_textbox = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//input[@type='text']")
        )
    )

    input_textbox[0].send_keys(address)
    input_textbox[1].send_keys(price)
    input_textbox[2].send_keys(link)

    submit_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Submit')]")
    submit_button.click()

    submit_again = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//a[@href='https://docs.google.com/forms/d/e/1FAIpQLSdg0WH0IqtED3tCSpCgkQX-W_SlKNqk5FL1-Qsv9eNGyfgVrA/viewform?usp=form_confirm']")
        )
    )

    submit_again.click()