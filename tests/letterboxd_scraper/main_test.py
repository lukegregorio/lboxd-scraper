import src.letterboxd_scraper.main

def test_load_script_tags():

    url = 'https://letterboxd.com/film/parasite-2019/'

    data = src.src.main.load_script_tags(url)

    assert data['name'] == 'Parasite'
    assert data['@type'] == 'Movie'