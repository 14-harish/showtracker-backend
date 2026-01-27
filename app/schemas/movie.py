from pydantic import BaseModel

class MovieCreate(BaseModel):
    tmdb_movie_id: int
    title: str
    release_year: int | None = None
    poster_path: str
    status: str  # watchlist, watching, completed
