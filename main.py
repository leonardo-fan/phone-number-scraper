import os
from dotenv import load_dotenv
from google import get_numbers_and_links_for_name
from basic_search import find_numbers_on_page
from linkedin import get_linkedin_profile_number

load_dotenv()

lkin_username = os.environ.get("LINKEDIN_USERNAME")
lkin_password = os.environ.get("LINKEDIN_PASSWORD")

print("Searching your Linkedin profile...")
if lkin_username and lkin_password:
    try:
        profile_url, lkin_numbers = get_linkedin_profile_number(lkin_username, lkin_password)
        print(profile_url, end=": ")
        print(lkin_numbers if lkin_numbers else 'No phone numbers found')
    except TimeoutError:
        print("Profile could not be found")

name = input("Please input your full name to search based on Google: ").strip()
google_links, link_grp = get_numbers_and_links_for_name(name)
print('https://www.google.com/:', google_links if google_links else 'No phone numbers found')

# remove linkedin domains as should be searched from before
for key in link_grp.copy():
    if "linkedin.com" in key:
        link_grp.pop(key)

search_links_goog = [link for grp in link_grp.values() for link in grp]
for link in search_links_goog:
    print(link, end=": ")
    print(find_numbers_on_page(link))
