import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

ACCOUNT_EMAIL = "cc@email.com"
ACCOUNT_PASSWORD = "password"
GYM_URL = "https://appbrewery.github.io/gym/"

options = Options()
options.add_experimental_option('detach', True)

user_data_dir = os.path.join(os.getcwd(), 'chrome_profile')
options.add_argument(f"--user-data-dir={user_data_dir}")

options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
driver = webdriver.Chrome(options=options)

driver.get(GYM_URL)

classes_booked = 0
waitlist_joined = 0
already_booked_waitlisted = 0
new_booking = []
new_waitlist = []

def login():
    #Click on login button
    login_button = driver.find_element(By.ID, value="login-button")
    login_button.click()
    #Enter email
    email_input = driver.find_element(By.ID, value="email-input")
    email_input.send_keys(ACCOUNT_EMAIL)
    #Enter password
    password_input = driver.find_element(By.ID, value="password-input")
    password_input.send_keys(ACCOUNT_PASSWORD)
    #Click on submit button
    submit_button = driver.find_element(By.ID, value="submit-button")
    submit_button.click()

def book_class():
    global classes_booked, waitlist_joined, already_booked_waitlisted

    wait = WebDriverWait(driver, 5)

    group_data = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div[id^='day-group']")
        )
    )

    for data in group_data:
        day_title = data.find_element(By.TAG_NAME, value="h2").text

        if "Tue" in day_title or "Thu" in day_title:
            class_schedule = data.find_element(By.CSS_SELECTOR, value="h2[id^='day-title']").text
            class_cards = data.find_elements(By.CSS_SELECTOR, value="div[id^='class-card']")

            for item in class_cards:
                time_class = item.find_element(By.CSS_SELECTOR, value="p[id^='class-time']").text

                if "6:00 PM" in time_class:
                    class_title = item.find_element(By.CSS_SELECTOR, value="h3[id^='class-name']").text
                    class_button = item.find_element(By.CSS_SELECTOR, value="button[id^='book-button']")

                    if "Booked" in class_button.text:
                        already_booked_waitlisted += 1

                        print(f"Class already booked: {class_title} - {class_schedule}")

                    elif "Waitlisted" in class_button.text:
                        already_booked_waitlisted += 1
                        print(f"Already on waitlist: {class_title} - {class_schedule}")

                    elif "Join Waitlist" in class_button.text:
                        class_button.click()
                        waitlist_joined += 1
                        join_waitlist = f"[New Waitlist] {class_title} on {class_schedule}"
                        new_waitlist.append(join_waitlist)
                        print(f"✓ Joined waitlist for: {class_title} - {class_schedule}")

                    else:
                        class_button.click()
                        classes_booked += 1
                        join_booking = f"[New Booking] {class_title} on {class_schedule}"
                        new_booking.append(join_booking)
                        print(f"✓ Successfully booked: {class_title} - {class_schedule}")

    total_tuesday_class = classes_booked + waitlist_joined + already_booked_waitlisted

    print(f"\n"
          f"--- BOOKING SUMMARY ---\n"
          f"New bookings: {classes_booked}\n"
          f"New waitlist entries: {waitlist_joined}\n"
          f"Already booked/waitlisted: {already_booked_waitlisted}\n"
          f"Total Tuesday & Thursday 6pm classes: {total_tuesday_class}")

    # print(f"\n--- DETAILED CLASS LIST ---")
    # print(*new_booking, sep="\n")
    # print(*new_waitlist, sep="\n")

def verify_booking():
    verified_bookings = 0
    verified_list = []

    bookings_button = driver.find_element(By.ID, value="my-bookings-link")
    bookings_button.click()

    booking_cards = driver.find_elements(By.CSS_SELECTOR, value="[id^='booking-card-booking']")

    for card in booking_cards:
        booked_class = card.find_element(By.CSS_SELECTOR, value="[id^='booking-class-name-booking']").text
        join_list = f"✓ Verified: {booked_class}"
        verified_list.append(join_list)
        verified_bookings += 1

    try:
        wait_list = []
        wait_section = driver.find_element(By.ID, value="waitlist-section")
        wait_cards = wait_section.find_elements(By.CSS_SELECTOR, value="[id^='waitlist-card-waitlist']")
        for card in wait_cards:
            class_title = card.find_element(By.CSS_SELECTOR, value="[id^='waitlist-class-name-waitlist']").text
            join_wait_list = f"✓ Verified: {class_title}"
            wait_list.append(join_wait_list)
            verified_bookings += 1

    except NoSuchElementException:
        pass

    print(f"\n--- VERIFYING ON MY BOOKINGS PAGE ---")
    print(*verified_list, sep="\n")
    if len(wait_list) > 0:
        print(*wait_list, sep="\n")

    print("\n--- VERIFICATION RESULT ---")
    print(f"Expected: {classes_booked + already_booked_waitlisted + waitlist_joined} bookings")
    print(f"Found: {verified_bookings} bookings/waitlist")

    total_booking = classes_booked + already_booked_waitlisted + waitlist_joined
    if total_booking != verified_bookings:
        difference = (classes_booked + already_booked_waitlisted + waitlist_joined) - verified_bookings
        print(f"❌ MISMATCH: Missing {difference} booking/s")

def run_bot_with_retry(max_retries=7):
    for attempt in range(max_retries):
        try:
            print(f"\n===== RUN ATTEMPT {attempt + 1} =====")

            login()
            book_class()
            verify_booking()

            print("\n✅ SUCCESS: Bot completed without errors")
            return

        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
            print(f"\n❌ Attempt {attempt + 1} failed: {e}")

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Retrying in {wait_time} seconds...\n")
                time.sleep(wait_time)

                # optional recovery step (refresh page)
                driver.refresh()

            else:
                print("\n🚨 All retries failed.")

run_bot_with_retry(7)