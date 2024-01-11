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


    def get_films(self) -> list[str]:
        """
        Get user watched films

        Returns
        -------
        list
            A list of film urls
        """

        user_root_films_url = self.url + "films/"

        page_urls = _get_pages(user_root_films_url)

        # get the film urls from each page
        film_urls = []

        for page_url in page_urls:
            film_urls += _get_film_from_poster(page_url)

        return film_urls


    def get_reviews(self) -> list[str]:
        """
        Get user reviews

        Returns
        -------
        list
            A list of reviews
        """

        review_url = self.url + "films/reviews/"

        page_urls = _get_pages(review_url)

        reviews = []

        for page_url in page_urls:
            reviews += _get_reviews_from_page(page_url)

        return reviews

    def get_watchlist(self) -> list[str]:
        pass

    def get_lists(self) -> list[str]:
        pass

    def get_followers(self) -> list[str]:
        """
        Get user followers

        Returns
        -------
        list
            A list of followers
        """

        followers_url = self.url + "followers/"

        page_urls = _get_pages(followers_url)

        followers = []

        for page_url in page_urls:
            followers += _get_followers_from_page(page_url)

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

        page_urls = _get_pages(following_url)

        following = []

        for page_url in page_urls:
            following += _get_following_from_page(page_url)

        return following

    @staticmethod
    def _get_pages(url: str) -> list[str]:
        """
        Get the pages of a page

        Parameters
        ----------
        url : str
            The url of the user's page

        Returns
        -------
        list
            A list of urls for each page of the user's films
        """

        user_films_html = requests.get(url).text

        soup = bs4.BeautifulSoup(user_films_html, "html.parser")

        page_links = soup.select('.paginate-pages a')

        last_page_number = int(page_links[-1].text)

        page_urls = [url + f'page/{page_number}/' for page_number in range(1, last_page_number)]

        return page_urls
    
    @staticmethod
    def _get_film_from_poster(url: str) -> str:
        """
        Get the film url from the poster on a user's films page

        Parameters
        ----------
        url : str
            The url of the user's films page

        Returns
        -------
        str
            The url of the film
        """

        page_html = requests.get(url).text

        soup = bs4.BeautifulSoup(page_html, "html.parser")

        film_soups = soup.find_all("li", {"class": "poster-container"})

        data_target_links = [div.get('data-target-link') for film in film_soups for div in film.find_all('div', {'data-target-link': True})]

        film_urls = ['https://letterboxd.com/' + partial_url for partial_url in data_target_links] 

        return film_urls
    
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

        page_html = requests.get(url).text

        soup = bs4.BeautifulSoup(page_html, "html.parser")

        div_list = soup.find_all("div", {"class": "body-text -prose collapsible-text"})

        reviews = [div.get_text(separator=' ', strip=True) for div in div_list]

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

        page_html = requests.get(url).text

        soup = bs4.BeautifulSoup(page_html, "html.parser")

        a_list = soup.find_all("a", {"class": "list-link"})

        lists = ['https://letterboxd.com' + list_soup.get('href') for list_soup in a_list]
        
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

        user_followers_html = requests.get(url).text

        soup = bs4.BeautifulSoup(user_followers_html, "html.parser")

        div_list = soup.find_all("div", {"class": "person-summary"})

        followers = ['https://letterboxd.com' + div.find("a", {"class": "name"}).get('href') for div in div_list]

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
        user_following_html = requests.get(url).text

        soup = bs4.BeautifulSoup(user_following_html, "html.parser")

        div_list = soup.find_all("div", {"class": "person-summary"})

        following = ['https://letterboxd.com' + div.find("a", {"class": "name"}).get('href') for div in div_list]

        return following
    
    pass


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