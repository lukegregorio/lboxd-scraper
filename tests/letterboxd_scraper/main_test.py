import letterboxd_scraper.main as letterboxd_scraper

def test_load_script_tags():

    url = 'https://letterboxd.com/film/parasite-2019/'

    data = letterboxd_scraper.load_script_tags(url)

    assert data['name'] == 'Parasite'
    assert data['@type'] == 'Movie'