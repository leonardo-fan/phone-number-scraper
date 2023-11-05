import os
from dotenv import load_dotenv
from google import get_numbers_and_links_for_names
from basic_search import find_numbers_on_page
from linkedin import get_linkedin_profile_numbers

def link_printer(link, verbose, numbers):
    if verbose or numbers:
        print(link, end=": ")
        print(numbers if numbers else NO_NUMBERS_PROMPT)

NO_NUMBERS_PROMPT = 'No phone numbers found'

load_dotenv()

verbose = False
lkin_username = os.environ.get("LINKEDIN_USERNAME")
lkin_password = os.environ.get("LINKEDIN_PASSWORD")

names = input("Please input your full name/aliases (comma separated) to search based on Google: ")\
    .strip()\
    .split(",")
related_levels = int(input("How many related search levels do you want?: "))

link_grp = get_numbers_and_links_for_names(names, related_levels)

linkedin_urls = []
for key in link_grp.copy():
    if "linkedin.com" in key:
        linkedin_urls.extend(link_grp[key])
        link_grp.pop(key)

search_links_goog = [link for grp in link_grp.values() for link in grp]
for link in search_links_goog:
    numbers = find_numbers_on_page(link)
    link_printer(link, verbose, numbers)

if lkin_username and lkin_password:
    print("Searching your Linkedin profile and using it to search profiles from Google...")
    try:
        this_profile_url, this_profile_number, other_profiles_numbers = \
            get_linkedin_profile_numbers(lkin_username, lkin_password, linkedin_urls)
        print("Given profile details from system", this_profile_url, end=": ")
        print(this_profile_number if this_profile_number else NO_NUMBERS_PROMPT)

        print("For linkedin profiles from Google... ")
        for profile_url, numbers in other_profiles_numbers.items():
            link_printer(profile_url, verbose, numbers)
    except TimeoutError:
        print("Your profile could not be found")
