import requests

from bs4 import BeautifulSoup
from random import choice
from time import sleep
from csv import DictWriter

URL = "http://quotes.toscrape.com"


def main(url=URL):
    print("Downloading new quotes...")
    all_scraped_quotes = get_pages_data(url)
    print(
        f"Done scraping {url} got a {type(all_scraped_quotes).__name__} of a {len(all_scraped_quotes)} quotes")
    save_to_csv(all_scraped_quotes)
    print("CSV file saved")


# SCRAPING FUNCTIONS


def save_to_csv(quotes):
    with open('quotes.csv', "w", encoding="utf-8") as csv_file:
        headers = ["quote", "author", "link"]
        csv_writer = DictWriter(csv_file, fieldnames=headers)
        csv_writer.writeheader()
        [csv_writer.writerow(quote) for quote in quotes]
            


def get_pages_data(url):
    """Scrapes all pages for quotes, finish when there is no next_button"""
    site_page = requests.get(url).content
    soup = make_soup(site_page)
    page_quotes = extract_quotes(soup)
    next_button = soup.find(class_="next")
    if next_button:
        # sleep(2)
        next_href = next_button.findChild("a")["href"]
        next_url = URL + next_href
        page_quotes.extend(get_pages_data(next_url))
    return page_quotes


def make_soup(site_page):
    """Parse the incoming html"""
    return BeautifulSoup(site_page, 'html.parser')


def extract_quotes(soup):
    """Grab all quotes from a single page and form a dictionary"""
    quotes = soup.find_all(class_="quote")
    page_quotes = []
    for q in quotes:
        children = q.findChildren()
        text = children[0].get_text()
        author = children[1].find(class_="author").get_text()
        bio_link = children[1].find("a")["href"]
        quote_data = {"quote": text, "author": author, "link": bio_link}
        page_quotes.append(quote_data)
    return page_quotes


if __name__ == "__main__":
    main(URL)
