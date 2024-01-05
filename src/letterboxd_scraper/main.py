import requests
import bs4
import json


class filmList:
    """
    A class to represent a list on Letterboxd
    """
    
    def __init__(self, url: str):
        self.url = url
        self.html = self.get_html()
        self.films = self.get_films()


    def get_html(self) -> str:
        """
        Get the HTML from the page of a letterboxd list

        Returns
        -------
        str
            The HTML from the page
        """

        response = requests.get(self.url)
        return response.text
    
    def get_films(self) -> list[str]:
        """
        Get the list of films from the HTML

        Returns
        -------
        list
            A list of films
        """

        soup = bs4.BeautifulSoup(self.html, "html.parser")
        return soup.select(".list-number+ a")


class User:
    """
    A class to represent a user on Letterboxd
    """
    
    def __init__(self, username: str):
        self.username = username
        self.url = f"https://letterboxd.com/{username}/"
    
    pass


class Film:
    """
    A class to represent a film on Letterboxd
    """
    
    def __init__(self, url: str):
        self.url = url
        self.data = self.load_script_tags()
        self.director = self.get_film_director()
        self.genre = self.get_film_genre()
        self.country = self.get_film_country()
        self.year = self.get_film_year()
        self.language = self.get_film_language()

            
    def load_script_tags(self) -> dict:
        """
        Load the script tags from the user's URL

        Returns
        -------
        dict
            A dict of script tags
        """

        soup = bs4.BeautifulSoup(requests.get(self.url).text, "html.parser")

        # get the script tag with the json data
        script_string = soup.find("script", type="application/ld+json").text

        # remove the CDATA tags
        script_string = (
            script_string.replace("/* <![CDATA[ */", "").replace("/* ]]> */", "").strip()
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

        details_html = requests.get(details_url).text

        # get tags for the details data on the url
        tags = (
            bs4.BeautifulSoup(details_html, "html.parser")
            .find("div", {"id": "tab-details"})
            .find_all("a", href=True)
        )

        # get the language
        language = [a.text for a in tags if a["href"].startswith("/films/language/")]

        return list(set(language))