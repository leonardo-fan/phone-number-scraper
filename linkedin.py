from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import url_contains
from phone_number import get_phone_numbers_from_string

def lkin_login(driver, username, password):
    # login with given credentials
    driver.get("https://www.linkedin.com/login")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "[type=submit]").click()
    # may need to authorize with code
    # below ensures a feed is navigated to
    wait = WebDriverWait(driver, timeout=120, poll_frequency=1)
    wait.until(url_contains("linkedin.com/feed/"))

def format_linkedin_urls(linkedin_urls):
    # linkedin urls must have www in the subdomain not the country code
    for i, url in enumerate(linkedin_urls):
        # get characters before first .
        dot_idx = url.find(".")
        if not url.startswith("https://www"):
            linkedin_urls[i] = "https://www" + linkedin_urls[i][dot_idx:]

def get_numbers_from_profile(driver, profile_url):
    driver.get(f"{profile_url}/overlay/contact-info/")

    # check for phone numbers in spans
    span_els = driver.find_elements(by=By.CSS_SELECTOR, value="span")
    return get_phone_numbers_from_string("".join([s.text for s in span_els]))

def get_this_profile_url_number(driver):
    driver.get("https://www.linkedin.com/in/")
    profile_url = driver.current_url
    if profile_url[-1] == "/":
        profile_url = profile_url[:-1]
    return profile_url, get_numbers_from_profile(driver, profile_url)

def get_linkedin_profile_numbers(username, password, linkedin_urls):
    # start session
    driver = webdriver.Chrome()
    # wait strategy
    driver.implicitly_wait(0.5)

    lkin_login(driver, username, password)

    this_profile_url, this_profile_number = get_this_profile_url_number(driver)

    other_profiles_numbers = {}
    format_linkedin_urls(linkedin_urls)
    for profile_url in linkedin_urls:
        other_profiles_numbers.update({
            profile_url: get_numbers_from_profile(driver, profile_url)
        })
    
    # end session
    driver.quit()

    return this_profile_url, this_profile_number, other_profiles_numbers
