from typing import Dict, List
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.franceculture.fr/emissions/la-conversation-scientifique"
france_culture_url = "https://www.franceculture.fr"


def get_episodes(podcast_url, france_culture_url) -> List:
    """
    This function takes in the url of a radio show from France Culture,
    looks for all the episodes of the show and, returns a dictionary with the name of the episodes as keys and
    the urls leading to that episode description on the website.
    """

    r = requests.get(podcast_url)
    soup = BeautifulSoup(r.content, "html.parser")

    ls_episodes = []
    for link in soup.find_all("a", "teaser-text"):
        dict_episodes = {}
        dict_episodes["Episode Title"] = link.get("title")
        dict_episodes["Episode URL"] = france_culture_url + link.get("href")
        ls_episodes.append(dict_episodes)

    return ls_episodes


def get_books(dict_books, france_culture_url) -> Dict:
    """
    This function takes the url of an episode as one input and the url of france culture as the other.
    It uses the episode's url to access the books listed on an episode's page and scrape their names and the urls
    to their page. It adds france culture's url to their href as it doesn't contain a usable link.
    """

    r_episode = requests.get(dict_books["Episode URL"])
    soup_episode = BeautifulSoup(r_episode.content, "html.parser")
    for book in soup_episode.find_all("a", "bibliography-content-book-text-title"):
        dict_books["Book Title"] = book.text
        dict_books["Book URL"] = france_culture_url + book.get("href")

    return dict_books


def get_book_information(dict_book) -> Dict:
    """
    This function takes the url of a book as one input.
    It allows us to access the book's page on France Culture.
    There, we can obtain a summary of the book and the name of its author.
    """
    try:
        r_book = requests.get(dict_book["Book URL"])
        soup_episode = BeautifulSoup(r_book.content, "html.parser")
        try:
            dict_book["Author"] = soup_episode.find(
                "div", "heading-zone-title-owner work"
            ).a.text
        except:
            dict_book["Author"] = soup_episode.find("div", "heading-zone-title-owner").text
        try:
            dict_book["Summary"] = soup_episode.find("div", "content-body").text
        except:
            dict_book["Summary"] = "Pas de résumé disponible. Désolé."

    except:
        dict_book["Author"] = "Pas de livre pour cette émission."
        dict_book["Summary"] = "Pas de livre pour cette émission."

    return dict_book


def main():
    ls_episodes = get_episodes(url, france_culture_url)
    ls_books_dict = [
        get_books(dict_episode, france_culture_url) for dict_episode in ls_episodes
    ]
    ls_books_with_information_dict = [
        get_book_information(dict_book) for dict_book in ls_books_dict
    ]
    df = pd.DataFrame(ls_books_with_information_dict)
    last_title = df[0:1]


if __name__ == "__main__":
    main()
