from google import get_numbers_and_links_for_name
from basic_search import find_numbers_on_page

name = input("Please input your full name to search: ").strip()
google_links, link_grp = get_numbers_and_links_for_name(name)
print('https://www.google.com/:', google_links if google_links else 'No phone numbers found')

search_links_goog = [link for grp in link_grp.values() for link in grp]
for link in search_links_goog:
    print(link, end=": ")
    print(find_numbers_on_page(link))
