from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import url_contains
from phone_number import get_phone_numbers_from_string

def get_linkedin_profile_number(username, password):
    # start session
    driver = webdriver.Chrome()
    # wait strategy
    driver.implicitly_wait(0.5)

    # login with given credentials
    driver.get("https://www.linkedin.com/login")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "[type=submit]").click()
    # may need to authorize with code
    # below ensures a feed is navigated to
    wait = WebDriverWait(driver, timeout=120, poll_frequency=1)
    wait.until(lambda _ : url_contains("linkedin.com/feed/"))

    # navigate to contact page
    driver.get("https://www.linkedin.com/in/")
    profile_url = driver.current_url
    driver.get(f"{profile_url}overlay/contact-info/")

    # check for phone numbers in spans
    span_els = driver.find_elements(by=By.CSS_SELECTOR, value="span")
    numbers = get_phone_numbers_from_string("".join([s.text for s in span_els]))

    # end session
    driver.quit()

    return profile_url, numbers
