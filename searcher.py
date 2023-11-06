import click
import os
from dotenv import load_dotenv
from basic_search import find_numbers_on_page
from google import get_numbers_and_links_for_names
from linkedin import get_linkedin_profile_numbers
from phone_number import get_phone_number_if_valid

NO_NUMBERS_PROMPT = 'No phone numbers found'

load_dotenv()
LINKEDIN_UNAME = os.environ.get("LINKEDIN_USERNAME")
LINKEDIN_PASS = os.environ.get("LINKEDIN_PASSWORD")

def links_printer(link_num_dict, verbose, mobile):
    found = 0
    matches = 0
    for link, nums in link_num_dict.items():
        if nums:
            found += 1
            if mobile and mobile in nums:
                matches += 1
            if (not mobile) or (mobile and mobile in nums):
                print(click.style(link, fg="green"), end=": ")
                print(click.style(nums, fg="white", bg="green"))
        elif verbose and not mobile:
            print(click.style(link, fg="magenta"), end=": ")
            print(click.style(NO_NUMBERS_PROMPT, fg="white", bg="magenta"))
    if found == 0:
        print(click.style("No links with phone numbers found", fg="yellow"))
    if mobile and matches == 0:
        print(click.style("No matches with given phone number found", fg="yellow"))

def linkedin_searcher(verbose, linkedin_urls, mobile):
    print(click.style("Searching your Linkedin profile and using it to search profiles from Google...", bold=True, overline=True))
    try:
        this_profile_url, this_profile_number, other_profiles_numbers = \
            get_linkedin_profile_numbers(LINKEDIN_UNAME, LINKEDIN_PASS, linkedin_urls)
        print(click.style(f"Given profile details from env {this_profile_url}: {this_profile_number if this_profile_number else NO_NUMBERS_PROMPT}", italic=True))

        # remove from links if seen from above
        other_profiles_numbers.pop(this_profile_url, '')

        print()
        print(click.style("For linkedin profiles from Google... ", underline=True))
        links_printer(other_profiles_numbers, verbose, mobile)
    except TimeoutError:
        print(click.style("Your profile could not be found", fg="red"))

@click.command()
@click.option('-v', '--verbose', default=False, is_flag=True,
              help='Show websites without phone numbers on it.')
@click.option('-n', '--names', required=True, multiple=True,
              help='"Name" to search for (can use flag multiple times for same person).')
@click.option('-m', '--number', help='Your phone number to filter for only matching numbers.')
@click.option('-r', '--rel_levels', 'related_levels', default=0, type=int,
              help='Number of recursive layers to do related searches for (may take a while).')
@click.option('-d', '--deep_search', default=False, is_flag=True,
              help=('Search through other Google search types '
                    'i.e. Videos, Images, etc. (may take a while).'))
@click.option('-l', '--linkedin', default=False, is_flag=True,
              help=('Enables LinkedIn searching. Must have a LinkedIn '
                    'profile to search with. Login information must be in a .env file in the cwd'))
def search_phone_numbers_on_name(verbose, names, number, related_levels, deep_search, linkedin):
    """
    Web scraper that finds phone numbers through links given by a Google search of someone's
    name/aliases. Has the ability to also look through LinkedIn profile information
    for phone numbers as well, if a LinkedIn profile is provided to search with.
    """
    mobile = None
    if number:
        mobile = get_phone_number_if_valid(number)
        if not mobile:
            print(click.style(("Provided phone number is invalid"), fg="red"))
            return

    if linkedin and (not LINKEDIN_UNAME or not LINKEDIN_PASS):
        print(click.style(("Add a .env file to the cwd with your LINKEDIN_USERNAME=... "
                           "and LINKEDIN_PASSWORD=..."), fg="red"))
        return

    link_grp = get_numbers_and_links_for_names(names, related_levels, deep_search)
    print(click.style("Getting related links to name from Google...", overline=True))

    linkedin_urls = []
    for key in link_grp.copy():
        if "linkedin.com" in key:
            linkedin_urls.extend(link_grp[key])
            link_grp.pop(key)

    search_links_goog = [link for grp in link_grp.values() for link in grp]
    g_link_to_number = {}
    with click.progressbar(search_links_goog, label='Searching links from Google') as p_bar:
        for link in p_bar:
            numbers = find_numbers_on_page(link)
            g_link_to_number[link] = numbers
    links_printer(g_link_to_number, verbose, mobile)

    print()
    if linkedin and LINKEDIN_UNAME and LINKEDIN_PASS:
        linkedin_searcher(verbose, linkedin_urls, mobile)

if __name__ == "__main__":
    search_phone_numbers_on_name()
