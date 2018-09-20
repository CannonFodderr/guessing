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
    player_won = play_round(quote)
    print('Nice!' if player_won else 'Too bad')
    play_again = input("Play again (y/n)?").lower()
    if not play_again in ("yes", "y"):
        return print("Bye Bye")
    game_loop(quotes)


def print_title():
    """Print game title"""
    print("*" * len(TITLE))
    print(TITLE)
    print("*" * len(TITLE))


def pick_random_quote(quotes):
    """Select a random quote from scraped list"""
    return choice(quotes)


def play_round(quote):
    """Play one round of guessing the author name"""
    strikes = 2
    quote_text = quote["quote"]
    author = quote["author"]
    print(author)
    name_list = split_full_name(author)
    author_bio = get_author_bio(quote)
    initials = get_initials(name_list)
    last_name_length = last_name_length_hint(name_list)
    hints = [last_name_length, initials, author_bio]
    user_guess = input(f"{quote_text}: ").lower()
    while strikes >= 0:
        if user_guess == author.lower():
            print(f"{author} is Correct!")
            return True
        elif user_guess != author.lower():
            print(f"No Sorry, Heres a hint: {hints[strikes]}")
            user_guess = input(
                f"Guess again, {strikes} strikes left: ").lower()
        strikes -= 1
    print(f"The correct answer was {author}")
    return False
        


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


def get_initials(name_list):
    """Return initials from the authors name"""
    return f"His/Hers initials are: {name_list[0][0]}.{name_list[1][0]}."


def last_name_length_hint(name_list):
    """Measure the length of the authors last name"""
    return f"Last name is {len(name_list[1])} charachters long"

def split_full_name(full_name):
    first_name, last_name = full_name.rsplit(" ", 1)
    return [first_name, last_name]

main()
