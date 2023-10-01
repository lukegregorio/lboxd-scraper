import requests
import bs4
import json

def load_script_tags(url):

    soup = bs4.BeautifulSoup(requests.get(url).text, 'html.parser')

    # get the script tag with the json data
    script_string = soup.find('script', type='application/ld+json').text   

    # remove the CDATA tags
    script_string = script_string.replace('/* <![CDATA[ */', '').replace('/* ]]> */', '').strip()

    data = json.loads(script_string)

    return data # a json object


def get_film_director(data):

    directors = []

    for dict in data['director']:
        directors.append(dict['name'])

    return directors # a list of director(s)


def get_film_genre(data):
    
    return data['genre'] # a list of genre(s)


def get_film_country(data):

    countries = []

    for dict in data['countryOfOrigin']:
        countries.append(dict['name'])

    return countries # a list of country(s)


def get_film_year(data):

    for dict in data['releasedEvent']:
        if dict['@type'] == 'PublicationEvent':
            return dict['startDate'] # a string of the year


def get_film_language(url):
    
    # get the html links to scrape for film info
    details_url = url + 'details'

    details_html = requests.get(details_url).text
    
    # get tags for the details data on the url
    tags = bs4.BeautifulSoup(details_html, 'html.parser').find('div', {'id':'tab-details'}).find_all('a', href=True)
    
    # get the language
    language = [a.text for a in tags if a['href'].startswith('/films/language/')]

    return list(set(language)) # a list of language(s) - remove duplicates


# letterboxd list functions

# Get the HTML from the page
def get_html(url):
    response = requests.get(url)
    return response.text


# Get the list of films from the HTML
def get_films(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    return soup.select('.list-number+ a')