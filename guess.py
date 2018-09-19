import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader

DB = 'quotes.csv'
URL = "http://quotes.toscrape.com"
TITLE = "How said the quote?"


def main():
    quotes = read_csv_file(DB)
    game_loop(quotes)

# GAME FUNCTIONS


def make_soup(site_page):
    """Parse the incoming html"""
    return BeautifulSoup(site_page, 'html.parser')


def read_csv_file(db):
    with open(db, "r", encoding="utf-8") as csv_file:
        csv_reader = DictReader(csv_file)
        return list(csv_reader)


def game_loop(quotes):
    """Start game once web scraping is done"""
    print_title()
    quote = pick_random_quote(quotes)
    game_over = play_round(quote)
    if game_over:
        play_again = input("Play again (y/n)?").lower()
        if play_again[0] == 'y':
            game_loop(quotes)


def print_title():
    """Print game title"""
    print("*" * len(TITLE))
    print(TITLE)
    print("*" * len(TITLE))


def pick_random_quote(quotes):
    """Select a random quote from scraped list"""
    rand_quote = choice(quotes)
    return rand_quote


def play_round(quote):
    """Play one round of guessing the author name"""
    strikes = 2
    quote_text = quote["quote"]
    author = quote["author"]
    author_bio = get_author_bio(quote)
    initials = get_initials(author)
    first_name_length = get_name_length(author)
    hints = [first_name_length, initials, author_bio]
    user_guess = input(f"Who said/wrote: {quote_text} ? ").lower()
    while True:
        if user_guess == author.lower():
            print(f"{author} is Correct!")
            return True
        elif user_guess != author.lower():
            print(f"No Sorry, Heres a hint: {hints[strikes]}")
            user_guess = input(
                f"Guess again, {strikes} strikes left: ").lower()
        if strikes == 0:
            print(f"The correct answer was {author}")
            return True
        strikes -= 1


def get_author_bio(quote):
    """Request content from author bio page and return a hint phrase"""
    bio_link = URL + quote["link"]
    bio_content = requests.get(bio_link).content
    if bio_content:
        soup = make_soup(bio_content)
        date = soup.find(class_="author-born-date").get_text()
        location = soup.find(class_="author-born-location").get_text()
        phrase = f"Born on {date} {location}"
        return phrase


def get_initials(author):
    """Return initials from the authors name"""
    name_list = author.split(" ")
    initials = f"His/Hers initials are: {name_list[0][0]}.{name_list[1][0]}."
    return initials


def get_name_length(author):
    """Measure the length of the authors last name"""
    name_list = author.split(" ")
    last_name_length = f"Last name is {len(name_list[1])} charachters long"
    return last_name_length


main()
