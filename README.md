# letterboxd-scraper

Get data from letterboxd in a flash. Example python repo project.

## Installation

```bash
pip install lboxd-scraper
```

## Usage

```python
from lboxd_scraper import lboxd
film = lboxd.Film("letterboxd.com/movie/parasite-2019/")
print(film.director)
``````
