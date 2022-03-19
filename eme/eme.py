"""
Silly app for my friend who unironically tracks every much he's ever watched
"""

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from helpers import add_movie, chunk, get_movies
from helpers import sanitize_movie_title as clean_title

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
        clean_movie_list = [clean_title(m) for m in movie_list]
        new_movie_needed = True
        for clean_movie_title in clean_movie_list:
            if clean_title(movie_query) in clean_movie_title:
                did_you_mean = Prompt.ask(f"Did you mean [i]{clean_movie_title}[/]?", choices=["y", "n"])
                if did_you_mean == "y":
                    console.print(f"[i]{movie_query}[/] is already on the list!")
                    new_movie_needed = False
                elif did_you_mean == "n":
                    new_movie_needed = True

        if new_movie_needed:
            add_movie(MOVIES_TXT_PATH, movie_query)
            console.print(f"Added [i]{movie_query}[/]!")
            new_movie_added = True

    if new_movie_added:
        movie_list = get_movies(MOVIES_TXT_PATH)

    for movie_title in movie_list:
        if len(movie_title) > 50:
            movies_table.add_row(Text(f"{movie_title} 🤔", overflow="fold"))
        else:
            movies_table.add_row(Text(f"{movie_title}", overflow="fold"))

    if new_movie_added:
        movies_table.caption = f"{len(movie_list) - 1} movies so far (w/ {movie_query} just added!)"
    else:
        movies_table.caption = f"{len(movie_list) - 1} movies so far"

    console.print(movies_table)
