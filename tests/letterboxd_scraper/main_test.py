from letterboxd_scraper.main import filmList, User, Film

# test letterboxd list methods

def test_get_html():

    film_list = filmList('https://letterboxd.com/gregs_pictures/list/lazed-out-summer/')

    html = film_list.get_html()

    assert html is not None


def test_get_films():

    film_list = filmList('https://letterboxd.com/gregs_pictures/list/lazed-out-summer/')

    films = film_list.get_films()

    expected_type = list

    assert isinstance(films, expected_type)


# test letterboxd film methods

def test_load_script_tags():

    film = Film('https://letterboxd.com/film/parasite-2019/')

    data = film.load_script_tags()

    assert data['name'] == 'Parasite'
    assert data['@type'] == 'Movie'


def test_get_film_director():

    film = Film('https://letterboxd.com/film/parasite-2019/')

    directors = film.get_film_director()

    assert directors == ['Bong Joon-ho']


def test_get_film_genre():

    film = Film('https://letterboxd.com/film/parasite-2019/')

    genres = film.get_film_genre()

    expected_type = list

    assert isinstance(genres, expected_type)


def test_get_film_country():

    film = Film('https://letterboxd.com/film/parasite-2019/')

    countries = film.get_film_country()

    expected_type = list

    assert isinstance(countries, expected_type)


def test_get_film_year():
    
    film = Film('https://letterboxd.com/film/parasite-2019/')
    
    year = film.get_film_year()
    
    assert year == '2019'


def test_get_film_language():

    film = Film('https://letterboxd.com/film/parasite-2019/')

    language = film.get_film_language()

    expected_type = list

    assert isinstance(language, expected_type)