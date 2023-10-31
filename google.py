from selenium import webdriver
from selenium.webdriver.common.by import By
from url_helper import group_links
from phone_number import get_phone_numbers_from_string

# blacklist
link_blacklist = {"https://www.google.com/search"}

def get_numbers_and_links_for_name(name):
    # start session
    driver = webdriver.Chrome()
    # wait strategy
    driver.implicitly_wait(0.5)
    # navigate to search results page
    driver.get(f"https://www.google.com/search?q={name}")

    # get search results
    search_res_cont = driver.find_element(by=By.ID, value="search")
    search_res_links_els = search_res_cont.find_elements(by=By.CSS_SELECTOR, value="a")
    links = [l.get_attribute("href") for l in search_res_links_els
            if any([(l.get_attribute("href")) and (l_b not in l.get_attribute("href"))
                    for l_b in link_blacklist])]

    links = list(dict.fromkeys(links))
    links_grp = group_links(links)

    # check for phone numbers in link descriptions
    search_res_span_els = search_res_cont.find_elements(by=By.CSS_SELECTOR, value="span")
    numbers = get_phone_numbers_from_string("".join([s.text for s in search_res_span_els]))

    # end session
    driver.quit()

    return (numbers, links_grp)
