from itertools import islice
from string import punctuation
from typing import Iterable


def chunk(it: Iterable, size: int):
    """Grabbed this of SO, lol"""
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def get_movies(movies_txt_path: str) -> list:
    """Creates list of movies"""
    with open(movies_txt_path, mode="r", encoding="UTF-8") as movies:
        return sorted(movies.read().splitlines())


def add_movie(movies_txt_path: str, movie_title: str) -> None:
    """Appends movie to movie list"""
    with open(movies_txt_path, mode="a", encoding="UTF-8") as movies:
        movies.write(f"{movie_title}\n")


def sanitize_movie_title(movie_title: str) -> str:
    """Removes punctuation and .lower()'s a movie title for easier comparison"""
    for mark in punctuation:
        movie_title = movie_title.replace(mark, "")
    return movie_title.lower()
