from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import invisibility_of_element
from selenium.common.exceptions import NoSuchElementException
from url_helper import group_links

# blacklist
LINK_BLACKLIST = {"imgres","policies.google.com","www.google.com/preferences",
                  "setprefs","support.google.com","accounts.google.com"}
SCROLL_TIMEOUT = 10
SCROLL_PAUSE_TIME = 1
SEARCH_QUERY_KEYWORD = "/search?"
CAPTCHA_TIMEOUT = 240
CAPTCHA_POLL = 3

def href_not_in_blacklist(href):
    return all([l_b not in href for l_b in LINK_BLACKLIST])

def scroll_to_page_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    wait = WebDriverWait(driver, timeout=SCROLL_TIMEOUT, poll_frequency=SCROLL_PAUSE_TIME)
    def same_scroll_height(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        nonlocal last_height
        same = new_height == last_height
        last_height = new_height
        return same
    wait.until(same_scroll_height)

def filter_links(link_els, links, related_search_links):
    for l in link_els:
        href = l.get_attribute("href")
        if href and SEARCH_QUERY_KEYWORD in href:
            related_search_links.add(href)
        elif href and href_not_in_blacklist(href):
            links.add(href)

def get_google_links_generic_page(driver, links, related_search_links):
    a_els = driver.find_elements(by=By.CSS_SELECTOR, value="a")
    filter_links(a_els, links, related_search_links)

def get_google_links_all_page(driver, links, related_search_links, deep_search):
    # get top search links
    search_cont = driver.find_element(by=By.ID, value="search")
    search_a_els = search_cont.find_elements(by=By.CSS_SELECTOR, value="a")
    if deep_search:
        # will add Google Images, Videos etc. to related links
        filter_links(search_a_els, links, related_search_links)
    else:
        for l in search_a_els:
            href = l.get_attribute("href")
            if href and href_not_in_blacklist(href):
                links.add(href)

    # get bottom elements and filter
    bottom_cont = driver.find_element(by=By.ID, value="botstuff")
    bottom_a_els = bottom_cont.find_elements(by=By.CSS_SELECTOR, value="a")
    filter_links(bottom_a_els, links, related_search_links)

def get_links_on_google_page(driver, related_levels, deep_search):
    if related_levels < 0:
        return []
    links = set()
    related_search_links = set()

    scroll_to_page_bottom(driver)

    try:
        get_google_links_all_page(driver, links, related_search_links, deep_search)
    except NoSuchElementException:
        # some query pages like images don't have the same ids as the "All" page
        get_google_links_generic_page(driver, links, related_search_links)

    # does related_levels number of search recursions
    if related_levels:
        for r_link in related_search_links:
            driver.get(r_link)
            links.update(get_links_on_google_page(driver, related_levels - 1, deep_search))

    return links

def get_search_query(names):
    names_quoted = [f"\"{name}\"" for name in names]
    names_q_str = "+".join(names_quoted)
    return f"https://www.google.com/search?as_oq={names_q_str}"

def wait_until_captcha_solved(driver):
    wait = WebDriverWait(driver, timeout=CAPTCHA_TIMEOUT, poll_frequency=CAPTCHA_POLL)
    try:
        captcha_el = driver.find_element(by=By.ID, value="captcha-form")
        wait.until(invisibility_of_element(captcha_el))
    except NoSuchElementException:
        pass

def get_numbers_and_links_for_names(names, related_levels, deep_search):
    # start session
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    # wait strategy
    driver.implicitly_wait(1)

    driver.get(get_search_query(names))

    wait_until_captcha_solved(driver)

    links_grp = group_links(list(get_links_on_google_page(driver, related_levels, deep_search)))

    # end session
    driver.quit()

    return links_grp
