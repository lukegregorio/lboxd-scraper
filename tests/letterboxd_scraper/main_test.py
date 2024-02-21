from letterboxd_scraper.main import Film, User, filmList


# test letterboxd user methods
    
def test_get_films():

    user = User('gregs_pictures')

    films = user.get_films()

    expected_type = dict

    assert isinstance(films, expected_type)


def test_get_reviews():
    
    user = User('gregs_pictures')

    reviews = user.get_reviews()

    expected_type = list

    assert isinstance(reviews, expected_type)


def test_get_lists():

    user = User('gregs_pictures')

    lists = user.get_lists()

    expected_type = list

    assert isinstance(lists, expected_type)


def test_get_followers():

    user = User('gregs_pictures')

    followers = user.get_followers()

    expected_type = list

    assert isinstance(followers, expected_type)


def test_get_following():

    user = User('gregs_pictures')

    following = user.get_following()

    expected_type = list

    assert isinstance(following, expected_type)


# test letterboxd user helper static methods
    
def test_get_pages():
    
        url = 'https://letterboxd.com/gregs_pictures/films/'
    
        pages = User._get_pages(url)
    
        expected_type = list
    
        assert isinstance(pages, expected_type)
        assert len(pages) > 0
        assert pages[1] == 'https://letterboxd.com/gregs_pictures/films/page/2/'


def test_find_next_page():
        
        url = 'https://letterboxd.com/myles154/following/'
    
        next_page = User._find_next_page(url)
    
        assert next_page == 'https://letterboxd.com/myles154/following/page/2/'

    
def test_get_film_from_poster():

    url = 'https://letterboxd.com/gregs_pictures/films/'

    films = User._get_film_from_poster(url)

    expected_type = dict

    assert isinstance(films, expected_type)


def test_get_reviews_from_page():

    url = 'https://letterboxd.com/gregs_pictures/films/reviews/page/1/'

    reviews = User._get_reviews_from_page(url)

    expected_type = list

    assert isinstance(reviews, expected_type)


def test_get_list_from_page():

    url = 'https://letterboxd.com/gregs_pictures/list/'

    films = User._get_list_from_page(url)

    expected_type = list

    assert isinstance(films, expected_type)


def test_get_followers_from_page():

    url = 'https://letterboxd.com/gregs_pictures/followers/page/1/'

    followers = User._get_followers_from_page(url)

    expected_type = list

    assert isinstance(followers, expected_type)
    

def test_get_following_from_page():
    
    url = 'https://letterboxd.com/gregs_pictures/following/page/1/'

    following = User._get_following_from_page(url)

    expected_type = list

    assert isinstance(following, expected_type)


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


def test_get_film_average_rating():
    
    film = Film('https://letterboxd.com/film/parasite-2019/')

    rating = film.get_film_average_rating()

    assert 0 < rating <= 5


def test_get_film_rating_count():
    
    film = Film('https://letterboxd.com/film/parasite-2019/')

    rating_count = film.get_film_rating_count()

    assert rating_count > 0


def test_get_top_film_reviews():

    film = Film('https://letterboxd.com/film/parasite-2019/')

    reviews = film.get_top_film_reviews()

    expected_type = list

    assert isinstance(reviews, expected_type)


# test letterboxd list methods

def test_get_films():

    film_list = filmList('https://letterboxd.com/gregs_pictures/list/lazed-out-summer/')

    films = film_list.get_films()

    expected_type = list

    assert isinstance(films, expected_type)