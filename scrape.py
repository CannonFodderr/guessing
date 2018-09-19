import requests
from bs4 import BeautifulSoup
from random import choice
from time import sleep
from csv import DictWriter

URL = "http://quotes.toscrape.com"
ALL_QUOTES = []
PLAY_AGAIN = True


def main(url):
    done_scraping = get_pages_data(url)
    if done_scraping:
        print(f"Done scraping {url}")
        save_to_csv(ALL_QUOTES)
        print("CSV file saved")


# SCRAPING FUNCTIONS


def save_to_csv(quotes):
    with open('quotes.csv', "w", encoding="utf-8") as csv_file:
        headers = ["quote", "author", "link"]
        csv_writer = DictWriter(csv_file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in ALL_QUOTES:
            csv_writer.writerow(quote)


def get_pages_data(url):
    """Scrapes all pages for quotes, finish when there is no next_button"""
    site_page = requests.get(url).content
    page_quotes = extract_quotes(site_page)
    add_quotes_to_list(page_quotes)
    next_page = check_for_next_page(site_page)
    if next_page == True:
        # sleep(2)
        return True
    return False


def add_quotes_to_list(page_quotes):
    """Adding a single page quotes to main quotes list"""
    for qoute in page_quotes:
        ALL_QUOTES.append(qoute)


def make_soup(site_page):
    """Parse the incoming html"""
    return BeautifulSoup(site_page, 'html.parser')


def check_for_next_page(site_page):
    """Check if next button exsists in page"""
    soup = make_soup(site_page)
    next_button = soup.find(class_="next")
    if next_button:
        next_href = next_button.findChild("a")["href"]
        next_url = URL + next_href
        get_pages_data(next_url)
        return True
    return False


def extract_quotes(site_page):
    """Grab all quotes from a single page and form a dictionary"""
    soup = make_soup(site_page)
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


main(URL)
