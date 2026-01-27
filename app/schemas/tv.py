from pydantic import BaseModel

class TVSave(BaseModel):
    tmdb_tv_id: int
    name: str
    first_air_year: int | None = None
    poster_path: str
    status: str  # watchlist | watching | completed
    current_season: int | None = None
    current_episode: int | None = None
