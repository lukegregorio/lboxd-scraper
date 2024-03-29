import requests
from bs4 import BeautifulSoup
import json

from typing import Union


class User:
    """
    A class to represent a user on Letterboxd
    """

    def __init__(self, username: str):
        self.username = username
        self.url = f"https://letterboxd.com/{username}/"
        self.films = self.get_films()
        self.reviews = self.get_reviews()
        self.lists = self.get_lists()
        self.followers = self.get_followers()
        self.following = self.get_following()

    def get_films(self) -> list[str]:
        """
        Get user watched films - iterate over letterboxd pages

        Returns
        -------
        dict
            returns a dict with info by each film url - includes user rating
        """

        user_root_films_url = self.url + "films/"

        page_urls = User._get_pages(user_root_films_url)

        # get the film urls from each page
        film_data = {}

        for page_url in page_urls:
            page_film_data = User._get_film_from_poster(page_url)
            film_data.update(page_film_data)

        return film_data

    def get_reviews(self) -> list[str]:
        """
        Get user reviews

        Returns
        -------
        list
            A list of reviews
        """

        review_url = self.url + "films/reviews/"

        page_urls = User._get_pages(review_url)

        reviews = []

        for page_url in page_urls:
            reviews += User._get_reviews_from_page(page_url)

        return reviews

    def get_lists(self) -> list[str]:
        """
        Get user lists

        Returns
        -------
        list
            A list of lists
        """

        list_url = self.url + "lists/"

        page_urls = User._get_pages(list_url)

        lists = []

        for page_url in page_urls:
            lists += User._get_list_from_page(page_url)

        return lists

    def get_followers(self) -> list[str]:
        """
        Get user followers

        Returns
        -------
        list
            A list of followers
        """

        followers_url = self.url + "followers/"

        followers = []

        while followers_url != None:
            followers += User._get_followers_from_page(followers_url)
            followers_url = User._find_next_page(followers_url)

        return followers

    def get_following(self) -> list[str]:
        """
        Get user following

        Returns
        -------
        list
            A list of following
        """

        following_url = self.url + "following/"

        following = []

        while following_url != None:
            following += User._get_following_from_page(following_url)
            following_url = User._find_next_page(following_url)

        return following

    @staticmethod
    def _get_pages(url: str) -> list[str]:
        """
        Get the pages of a page for pages with numbers at the bottom of the page. Works for user's films, reviews, lists.

        Parameters
        ----------
        url : str
            The url of the user's page

        Returns
        -------
        list
            A list of urls for each page to scrape
        """

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        page_links = soup.select(".paginate-pages a")

        if len(page_links) == 0:
            # if there is only one page
            return [url]
        else:
            last_page_number = int(page_links[-1].text)
            page_urls = [
                url + f"page/{page_number}/"
                for page_number in range(1, last_page_number)
            ]
            return page_urls

    @staticmethod
    def _find_next_page(url: str) -> Union[str, None]:
        """
        Check if there is a next page. Works for user's followers and following.

        Parameters
        ----------
        url : str
            The url of the user's page

        Returns
        -------
        str or None
            The url of the next page or None if there is no next page
        """

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        next_page = soup.find("a", {"class": "next"})

        if next_page != None:
            return "https://letterboxd.com" + next_page.get("href")
        else:
            return None

    @staticmethod
    def _get_film_from_poster(url: str) -> str:
        """
        Get the film url and user rating from the poster on a user's films page

        Parameters
        ----------
        url : str
            The url of the user's films page

        Returns
        -------
        film_data : dict
        """

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        film_soups = soup.find_all("li", {"class": "poster-container"})

        # store film url and rating
        film_data = {}

        for film in film_soups:
            # get url of film
            div = film.find("div", class_="linked-film-poster")
            film_url = "https://letterboxd.com" + div.get("data-target-link")

            # get rating of film
            rating_span = film.find("span", class_="rating")
            # check if rating is available
            if rating_span:
                # get rating
                class_attribute = rating_span["class"]
                for attribute in class_attribute:
                    if "rated-" in attribute:
                        film_rating = (
                            int(attribute.split("rated-")[-1]) / 2
                        )  # convert to 5 star scale from 10 star scale
            else:
                film_rating = None

            film_data[film_url] = {"rating": film_rating}

        return film_data

    @staticmethod
    def _get_reviews_from_page(url: str) -> list[str]:
        """
        Get the reviews from a page

        Parameters
        ----------
        url : str
            The url of the user's reviews page

        Returns
        -------
        list
            A list of reviews
        """

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        div_list = soup.find_all("div", {"class": "body-text -prose collapsible-text"})

        reviews = [div.get_text(separator=" ", strip=True) for div in div_list]

        return reviews

    @staticmethod
    def _get_list_from_page(url: str) -> list[str]:
        """
        Get the lists from a page

        Parameters
        ----------
        url : str
            The url of the user's lists page

        Returns
        -------
        list
            A list of lists
        """

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        a_list = soup.find_all("a", {"class": "list-link"})

        lists = [
            "https://letterboxd.com" + list_soup.get("href") for list_soup in a_list
        ]

        return lists

    @staticmethod
    def _get_followers_from_page(url: str) -> list[str]:
        """
        Get the followers from a page

        Parameters
        ----------
        url : str
            The url of the user's followers page

        Returns
        -------
        list
            A list of followers
        """

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        div_list = soup.find_all("div", {"class": "person-summary"})

        followers = [
            "https://letterboxd.com" + div.find("a", {"class": "name"}).get("href")
            for div in div_list
        ]

        return followers

    @staticmethod
    def _get_following_from_page(url: str) -> list[str]:
        """
        Get the following from a page

        Parameters
        ----------
        url : str
            The url of the user's following page

        Returns
        -------
        list
            A list of following
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        div_list = soup.find_all("div", {"class": "person-summary"})

        following = [
            "https://letterboxd.com" + div.find("a", {"class": "name"}).get("href")
            for div in div_list
        ]

        return following


class Film:
    """
    A class to represent a film on Letterboxd
    """

    def __init__(self, url: str):
        self.url = url
        self.data = self.load_script_tags()
        self.title = self.data["name"]
        self.director = self.get_film_director()
        self.genre = self.get_film_genre()
        self.country = self.get_film_country()
        self.year = self.get_film_year()
        self.language = self.get_film_language()
        self.average_rating = self.get_film_average_rating()
        self.rating_count = self.get_film_rating_count()
        self.description = self.get_film_description()
        self.reviews = self.get_top_film_reviews()

    def load_script_tags(self) -> dict:
        """
        Load the script tags from the user's URL

        Returns
        -------
        dict
            A dict of script tags
        """

        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        # get the script tag with the json data
        script_string = soup.find("script", type="application/ld+json").text

        # remove the CDATA tags
        script_string = (
            script_string.replace("/* <![CDATA[ */", "")
            .replace("/* ]]> */", "")
            .strip()
        )

        data = json.loads(script_string)

        return data

    def get_film_director(self) -> list:
        """
        Get the director(s) of the film

        Returns
        -------
        list
            A list of director(s)
        """

        directors = []

        for dict in self.data["director"]:
            directors.append(dict["name"])

        return directors

    def get_film_genre(self) -> list:
        """
        Get the genre(s) of the film

        Returns
        -------
        list
            A list of genre(s)
        """

        return self.data["genre"]

    def get_film_country(self) -> list:
        """
        Get the country(s) of the film

        Returns
        -------
        list
            A list of country(s)
        """

        countries = []

        for dict in self.data["countryOfOrigin"]:
            countries.append(dict["name"])

        return countries

    def get_film_year(self) -> str:
        """
        Get the year the film was released

        Returns
        -------
        str
            A string of the year
        """

        for dict in self.data["releasedEvent"]:
            if dict["@type"] == "PublicationEvent":
                return dict["startDate"]

    def get_film_language(self) -> list:
        """
        Get the language(s) of the film

        Returns
        -------
        list
            A list of language(s)
        """

        # get the html links to scrape for film info
        details_url = self.url + "details"

        response = requests.get(details_url)
        soup = BeautifulSoup(response.content, "html.parser")

        # get tags for the details data on the url
        tags = soup.find("div", {"id": "tab-details"}).find_all("a", href=True)

        # get the language
        language = [a.text for a in tags if a["href"].startswith("/films/language/")]

        return list(set(language))

    def get_film_average_rating(self) -> float:
        """
        Get the average rating of the film

        Returns
        -------
        float
            The average rating of the film
        """

        return self.data["aggregateRating"]["ratingValue"]

    def get_film_rating_count(self) -> int:
        """
        Get the number of ratings of the film

        Returns
        -------
        int
            The number of ratings of the film
        """

        return self.data["aggregateRating"]["ratingCount"]

    def get_film_description(self) -> str:
        """
        Get the summary of the film

        Returns
        -------
        str
            The description of the film
        """

        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        description = soup.select_one("div.truncate > p").text

        return description

    def get_top_film_reviews(self) -> list:
        """
        Get the top reviews of the film

        Returns
        -------
        list
            A list of top reviews from the first page of most popular reviews
        """

        reviews_url = self.url + "reviews/by/activity/"

        response = requests.get(reviews_url)
        soup = BeautifulSoup(response.content, "html.parser")

        div_list = soup.find_all("div", {"class": "body-text -prose collapsible-text"})

        reviews = [div.get_text(separator=" ", strip=True) for div in div_list]

        return reviews


class filmList:
    """
    A class to represent a list on Letterboxd
    """

    def __init__(self, url: str):
        self.url = url
        self.films = self.get_films()

    def get_films(self) -> list[str]:
        """
        Get the list of films from the HTML

        Returns
        -------
        list
            A list of films
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.select(".list-number+ a")
