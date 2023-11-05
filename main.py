import click
import os
from dotenv import load_dotenv
from google import get_numbers_and_links_for_names
from basic_search import find_numbers_on_page
from linkedin import get_linkedin_profile_numbers

NO_NUMBERS_PROMPT = 'No phone numbers found'

load_dotenv()
LINKEDIN_UNAME = os.environ.get("LINKEDIN_USERNAME")
LINKEDIN_PASS = os.environ.get("LINKEDIN_PASSWORD")

def links_printer(link_num_dict, verbose):
    matches = 0
    for link, nums in link_num_dict.items():
        if nums:
            matches += 1
            print(link, end=": ")
            print(click.style(nums, fg="cyan"))
        elif verbose:
            print(link, end=": ")
            print(click.style(NO_NUMBERS_PROMPT, fg="magenta"))
    if matches == 0:
        print(click.style("No links with phone numbers found", fg="yellow"))

def linkedin_searcher(verbose, linkedin_urls):
    print(click.style("Searching your Linkedin profile and using it to search profiles from Google...", bold=True))
    try:
        this_profile_url, this_profile_number, other_profiles_numbers = \
            get_linkedin_profile_numbers(LINKEDIN_UNAME, LINKEDIN_PASS, linkedin_urls)
        print(click.style(f"Given profile details from env {this_profile_url}: {this_profile_number if this_profile_number else NO_NUMBERS_PROMPT}", italic=True))

        # remove from links if seen from above
        other_profiles_numbers.pop(this_profile_url, '')

        print()
        print(click.style("For linkedin profiles from Google... ", underline=True))
        links_printer(other_profiles_numbers, verbose)
    except TimeoutError:
        print(click.style("Your profile could not be found", fg="red"))

@click.command()
@click.option('-v', '--verbose', default=False, show_default=True, is_flag=True,
              help='Show websites without phone numbers on it.')
@click.option('-n', '--names', required=True, multiple=True,
              help='"Name" to search for (can use flag multiple times for same person).')
@click.option('-r', '--rel_levels', 'related_levels', default=0, type=int,
              help='Number of recursive layers to do related searches for (may take a while).')
@click.option('-d', '--deep_search', default=False,
              help='Search through other Google search types \
                i.e. Videos, Images, etc. (may take a while).')
@click.option('-l', '--linkedin', default=False, show_default=True, is_flag=True,
              help='Enables LinkedIn searching. Must have a LinkedIn Profile to search with')
def search_phone_numbers_on_name(verbose, names, related_levels, deep_search, linkedin):
    link_grp = get_numbers_and_links_for_names(names, related_levels, deep_search)

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
    links_printer(g_link_to_number, verbose)

    print()
    if linkedin and LINKEDIN_UNAME and LINKEDIN_PASS:
        linkedin_searcher(verbose, linkedin_urls)
    elif linkedin:
        print(click.style("Add a .env file to the directory with your LINKEDIN_USERNAME=... and LINKEDIN_PASSWORD=...", fg="red"))

if __name__ == "__main__":
    search_phone_numbers_on_name()
