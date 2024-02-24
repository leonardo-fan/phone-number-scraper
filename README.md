# Personal Phone Number Scraper

This is a Command Line Interface (CLI) that aims to show users if their phone number is publicly accessible on Google and/or if it is available on the sites linked through Google. It also doubles as a tool that can find phone numbers across Google given specific search terms.

## Usage
```
python3 searcher.py [OPTIONS]
```

Use the --help option to show more information about the program.

![--help option screenshot](/phone-number-scraper-demo-h.png)

The CLI takes a variable amount of name options which creates and sends a search query to Google. From this search, all the available links are opened and the text within the website is searched through for phone numbers. If a phone number string is given to the “-m” option, a site will only show in the output if a match is found for the given number. 

The search can also be expanded through the “-r” and “-d” options. When a search is done (root node), there are related searches given by Google (children of the root), by using the “-r” option with a number x, the program will search through x levels of related searches (children). By using the “-d” flag, other types of Google searches will be added to the related searches like Google Images, Shopping, Videos etc.

The “-l” flag will also enable LinkedIn search (provided a .env file is added to the directory with a user’s valid LinkedIn username and password). It first searches the user’s profile for phone numbers, then using any LinkedIn profiles found from the Google query, it will automate the user’s account to search these profiles and look for any phone numbers present in them.

“-v” will turn on verbose mode, giving more information about all the links searched, which includes sites without any phone numbers on them.

## Setup
1. Have Python 3.x installed.
2. Clone this git repository.
3. Create a virtualenv.
4. Install ```requirements.txt```.
5. Add a ```.env``` file to your current working directory with your LinkedIn login information. Replace "..." with your information.
```
LINKEDIN_USERNAME=...
LINKEDIN_PASSWORD=...
```
6. Run the program.
```
python3 searcher.py [OPTIONS]
```
