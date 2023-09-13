import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

user_phone = input("What is your LinkedIn phone number? ")
user_pass = input("What is your LinkedIn password? ")

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs&position=1&pageNum=0")

driver.maximize_window()

login = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav__cta-container .btn-secondary-emphasis")))
login.click()

email_login = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "username")))
pass_login = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "password")))

email_login.send_keys(user_phone)
pass_login.send_keys(user_pass)

sign_button = driver.find_element(By.CSS_SELECTOR, value=".login__form_action_container .btn__primary--large")
sign_button.click()

time.sleep(8)

job_listings = driver.find_elements(By.CSS_SELECTOR, value='.job-card-container--clickable')

for job in job_listings:
    job.click()
    time.sleep(3)
    try:
        apply_but = driver.find_element(By.CSS_SELECTOR, value='.job-card-container--clickable')
    except NoSuchElementException:
        print("Could not find apply button, moving on to next job listing.")
        continue
    else:
        apply_but.click()
        phone_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "fb-single-line-text__input")))
        if not phone_input.text:
            phone_input.send_keys(user_phone)
        submit_app = driver.find_element(By.CSS_SELECTOR, value="footer button")

        if submit_app.get_attribute("data-control-name") == "continue_unify":
            close_tab = driver.find_element(By.CLASS_NAME, value = 'artdeco-modal__dismiss')
            close_tab.click()
            time.sleep(2)
            discard_button = driver.find_elements(By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")
            discard_button[1].click()
            print("Skipped app for complex applying steps")
            continue
        else:
            submit_app.click()

        close_app = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-modal__dismiss")))
        close_app.click()

time.sleep(3)
driver.quit()


