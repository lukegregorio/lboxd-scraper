from letterboxd_scraper.main import filmList, User, Film

# test letterboxd list methods

def test_get_html():

    film_list = filmList('https://letterboxd.com/gregs_pictures/list/lazed-out-summer/')

    html = film_list.get_html(film_list.url)

    assert html is not None


def test_get_films():

    url = 'https://letterboxd.com/gregs_pictures/list/lazed-out-summer/'

    html = letterboxd_scraper.get_html(url)

    films = letterboxd_scraper.get_films(html)

    expected_type = list

    assert isinstance(films, expected_type)


# test letterboxd film methods

def test_load_script_tags():

    url = 'https://letterboxd.com/film/parasite-2019/'

    data = letterboxd_scraper.load_script_tags(url)

    assert data['name'] == 'Parasite'
    assert data['@type'] == 'Movie'


def test_get_film_director():

    url = 'https://letterboxd.com/film/parasite-2019/'

    data = letterboxd_scraper.load_script_tags(url)

    directors = letterboxd_scraper.get_film_director(data)

    assert directors == ['Bong Joon-ho']


def test_get_film_genre():

    url = 'https://letterboxd.com/film/parasite-2019/'

    data = letterboxd_scraper.load_script_tags(url)

    genres = letterboxd_scraper.get_film_genre(data)

    expected_type = list

    assert isinstance(genres, expected_type)


def test_get_film_country():

    url = 'https://letterboxd.com/film/parasite-2019/'

    data = letterboxd_scraper.load_script_tags(url)

    countries = letterboxd_scraper.get_film_country(data)

    expected_type = list

    assert isinstance(countries, expected_type)


def test_get_film_year():
    
        url = 'https://letterboxd.com/film/parasite-2019/'
    
        data = letterboxd_scraper.load_script_tags(url)
    
        year = letterboxd_scraper.get_film_year(data)
        
        assert year == '2019'


def test_get_film_language():

    url = 'https://letterboxd.com/film/parasite-2019/'

    language = letterboxd_scraper.get_film_language(url)

    expected_type = list

    assert isinstance(language, expected_type)