import requests
from bs4 import BeautifulSoup


# Sends a GET request to the given URL, and returns a parsed version of the page
def scrape_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup
