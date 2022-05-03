from typing import Dict, List
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_all_episodes_pages(podcast_name, france_culture_url) -> List:
    page_exists = True
    ls_pages_urls = []
    i = 1
    while page_exists:
        page_parameter = f"?p={i}"
        page_url = france_culture_url + podcast_name + page_parameter
        r = requests.get(
            page_url
        )  # If this returns an error then we go to the exception and break our loop. Better way to do this?
        if r.status_code == 200:
            ls_pages_urls.append(page_parameter)
            i += 1
        else:
            page_exists = False

    return ls_pages_urls


def get_episodes(podcast_name, france_culture_url, page_parameter) -> List:
    """
    This function takes in the url of a radio show from France Culture,
    looks for all the episodes of the show and, returns a list containing a dictionary for each episode with its title and url.
    """

    r = requests.get(france_culture_url + podcast_name + page_parameter)
    soup = BeautifulSoup(r.content, "html.parser")

    ls_episodes = []
    for link in soup.find_all("a", "teaser-text"):
        dict_episode = {}
        dict_episode["Episode Title"] = link.get("title")
        dict_episode["Episode URL"] = france_culture_url + link.get("href")
        ls_episodes.append(dict_episode)

    return ls_episodes


def get_books(dict_episode, france_culture_url) -> List:
    """
    This function takes an episode dictionary as one input and the url of france culture as the other.
    It uses the episode's url to access the books listed on an episode's page and scrape their names and the urls
    to their page. It adds france culture's url to their href as it doesn't contain a usable link.
    It return a list containing a dictionary for each book discussed in the episode.
    """

    r_episode = requests.get(dict_episode["Episode URL"])
    soup_episode = BeautifulSoup(r_episode.content, "html.parser")
    ls_dict_books = []
    for book in soup_episode.find_all("a", "bibliography-content-book-text-title"):
        print(book)
        dict_episode["Book Title"] = book.text
        dict_episode["Book URL"] = france_culture_url + book.get("href")
        ls_dict_books.append(dict_episode)

    return ls_dict_books


def get_book_information(dict_book) -> List:
    """
    This function takes a book dictionary as input.
    It allows us to access the book's page on France Culture.
    There, we can obtain a summary of the book and the name of its author.
    It returns a
    """
    # ls_books = []
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
        # ls_books.append(dict_book)
    except:
        dict_book["Book URL"] = "Pas de livre pour cette émission"
        dict_book["Author"] = "Pas de livre pour cette émission."
        dict_book["Summary"] = "Pas de livre pour cette émission."
        # ls_books.append(dict_book)

    return dict_book


def main():

    podcast_name = "/emissions/la-conversation-scientifique"
    france_culture_url = "https://www.franceculture.fr"

    ls_pages_url = get_all_episodes_pages(podcast_name, france_culture_url)
    ls_episodes = [
        get_episodes(podcast_name, france_culture_url, page_parameter)
        for page_parameter in ls_pages_url
    ]
    flat_list_episodes = [item for sublist in ls_episodes for item in sublist]

    ls_books_dict = [
        get_books(dict_episode, france_culture_url) for dict_episode in flat_list_episodes
    ]
    flat_list_books_dict = [item for sublist in ls_books_dict for item in sublist]
    ls_books_with_information_dict = [
        get_book_information(dicta) for dicta in flat_list_books_dict
    ]
    # flat_list2 = [item for sublist in ls_books_with_information_dict for item in sublist]

    df = pd.DataFrame(ls_books_with_information_dict)
    print(df)


if __name__ == "__main__":
    main()
