import requests
from bs4 import BeautifulSoup
from random import choice

URL = "http://quotes.toscrape.com"
ALL_QUOTES = []
TITLE = "How said the quote?"
PLAY_AGAIN = True


def main(url):
    done_scraping = get_pages_data(url)
    if done_scraping:
        game_loop()

# GAME FUNCTIONS


def game_loop():
    """Start game once web scraping is done"""
    print_title()
    quote = pick_random_quote()
    game_over = play_round(quote)
    if game_over:
        play_again = input("Play again (y/n)?").lower()
        if play_again[0] == 'y':
            game_loop()


def print_title():
    """Print game title"""
    print("*" * len(TITLE))
    print(TITLE)
    print("*" * len(TITLE))


def pick_random_quote():
    """Select a random quote from scraped list"""
    rand_quote = choice(ALL_QUOTES)
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

# SCRAPING FUNCTIONS


def get_pages_data(url):
    """Scrapes all pages for quotes, finish when there is no next_button"""
    site_page = requests.get(url).content
    page_quotes = extract_quotes(site_page)
    add_quotes_to_list(page_quotes)
    next_page = check_for_next_page(site_page)
    if next_page == True:
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
