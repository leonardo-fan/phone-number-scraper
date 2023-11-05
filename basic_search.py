import requests
from bs4 import BeautifulSoup
from phone_number import get_phone_numbers_from_string

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}

def find_numbers_on_page(link):
    # timeout in seconds
    try:
        res = requests.get(link, headers=headers, data={}, timeout=10).text
    except:
        return 'Request Error'
    soup = BeautifulSoup(res, 'html.parser')
    phone_numbers = get_phone_numbers_from_string(soup.get_text())
    return phone_numbers if phone_numbers else []
