import requests
import bs4
import json

def load_script_tags(url):
    """
    Load the script tags from the url

    Parameters
    ----------
    url : str
        The url to scrape

    Returns
    -------
    list
        A list of script tags
    """

    soup = bs4.BeautifulSoup(requests.get(url).text, 'html.parser')

    # get the script tag with the json data
    script_string = soup.find('script', type='application/ld+json').text   

    # remove the CDATA tags
    script_string = script_string.replace('/* <![CDATA[ */', '').replace('/* ]]> */', '').strip()

    data = json.loads(script_string)

    return data


def get_film_director(data):
    """
    Get the director(s) of the film
    
    Parameters
    ----------
    data : dict
        The data from the script tag
        
    Returns
    -------
    list
        A list of director(s)
    """

    directors = []

    for dict in data['director']:
        directors.append(dict['name'])

    return directors


def get_film_genre(data):
    """
    Get the genre(s) of the film
    
    Parameters
    ----------
    data : dict
        The data from the script tag
    
    Returns
    -------
    list
        A list of genre(s)
    """
    
    return data['genre'] 


def get_film_country(data):
    """
    Get the country(s) of the film

    Parameters
    ----------
    data : dict
        The data from the script tag

    Returns
    -------
    list
        A list of country(s)
    """

    countries = []

    for dict in data['countryOfOrigin']:
        countries.append(dict['name'])

    return countries 


def get_film_year(data):
    """
    Get the year the film was released

    Parameters
    ----------
    data : dict
        The data from the script tag

    Returns
    -------
    str
        A string of the year
    """

    for dict in data['releasedEvent']:
        if dict['@type'] == 'PublicationEvent':
            return dict['startDate']


def get_film_language(url):
    """
    Get the language(s) of the film

    Parameters
    ----------
    url : str
        The url to scrape

    Returns
    -------
    list
        A list of language(s)
    """
    
    # get the html links to scrape for film info
    details_url = url + 'details'

    details_html = requests.get(details_url).text
    
    # get tags for the details data on the url
    tags = bs4.BeautifulSoup(details_html, 'html.parser').find('div', {'id':'tab-details'}).find_all('a', href=True)
    
    # get the language
    language = [a.text for a in tags if a['href'].startswith('/films/language/')]

    return list(set(language))


# letterboxd list functions

# Get the HTML from the page
def get_html(url):
    """
    Get the HTML from the page
    
    Parameters
    ----------
    url : str
        The url to scrape
        
    Returns
    -------
    str
        The HTML from the page
    """

    response = requests.get(url)
    return response.text


# Get the list of films from the HTML
def get_films(html):
    """
    Get the list of films from the HTML

    Parameters
    ----------
    html : str
        The HTML from the page

    Returns
    -------
    list
        A list of films
    """

    soup = bs4.BeautifulSoup(html, 'html.parser')
    return soup.select('.list-number+ a')