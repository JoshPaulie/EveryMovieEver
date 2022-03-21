"""
Silly app for my friend who unironically tracks every much he's ever watched
"""
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from thefuzz import process

from helpers import add_movie, get_movies

console = Console()

# Construct and style table
movies_table = Table(show_header=False, box=box.ROUNDED)
movies_table.add_column("movies")
movies_table.row_styles = ["", "cornsilk1"]


if __name__ == "__main__":

    console.print(
        Panel(
            "Add a movie below, or enter nothing to see the list in all its glory ✨",
            title="🎥 Every Movie Ever!",
        )
    )

    movie_query = Prompt.ask("[sea_green3]Enter a movie title[/]")
    MOVIES_TXT_PATH = "eme/movies.txt"
    movie_list = get_movies(MOVIES_TXT_PATH)
    new_movie_added = False

    if movie_query:
        new_movie_needed = True
        title_matches = process.extractBests(movie_query, movie_list, score_cutoff=75)

        if title_matches:
            for match in title_matches:
                did_you_mean = Prompt.ask(f"Did you mean [i]{match[0]}[/]?", choices=["y", "n", "add"])

                match did_you_mean:
                    case "y":
                        console.print(f"[i]{movie_query}[/] is already on the list!")
                        new_movie_needed = False
                    case "n":
                        new_movie_needed = True
                    case "add":
                        new_movie_needed = True
                        break

        """
        ? Why this weird, boolean pass-off? (new_movie_needed & new_movie_added)
        In my head, every title should be checked before adding a new one,
        and not just stopping at the first close match. Open to suggests.
        """
        if new_movie_needed:
            add_movie(MOVIES_TXT_PATH, movie_query)
            console.print(f"Added [i]{movie_query}[/]!")
            new_movie_added = True

    if new_movie_added:
        movie_list = get_movies(MOVIES_TXT_PATH)

    for movie_title in movie_list:
        # He likes to add long descriptions for movies he can't
        # remember the title of, which 'should' be distinguished
        movies_table.add_row(
            Text(f"{movie_title} 🤔" if len(movie_title) > 50 else movie_title, overflow="fold")
        )

    caption = f"{len(movie_list) - 1} movies so far 🍿"
    if new_movie_added:
        caption += f" (w/ {movie_query} just added!)"
    movies_table.caption = caption

    console.print(movies_table)
