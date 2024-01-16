import requests
from bs4 import BeautifulSoup

def get_soup(url):
    """
    Get a BeautifulSoup object from a URL.

    Parameters
    ----------
    url : str
        A URL.

    Returns
    -------
    soup : BeautifulSoup
        A BeautifulSoup object.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup