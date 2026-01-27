from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.auth.dependencies import get_current_user
from app.models.movie import Movie
from app.models.user_movie import UserMovie
from app.models.tv_show import TVShow
from app.models.user_tv_show import UserTVShow

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # ----- MOVIES -----
    movies = db.query(UserMovie, Movie).join(
        Movie, UserMovie.movie_id == Movie.id
    ).filter(
        UserMovie.user_id == current_user.id
    ).all()

    movies_data = {
        "watchlist": [],
        "watching": [],
        "completed": []
    }

    for um, m in movies:
        movies_data[um.status].append({
            "tmdb_movie_id": m.tmdb_movie_id,
            "title": m.title,
            "release_year": m.release_year,
            "poster_path": m.poster_path
        })

    # ----- TV SHOWS -----
    tv_shows = db.query(UserTVShow, TVShow).join(
        TVShow, UserTVShow.tv_show_id == TVShow.id
    ).filter(
        UserTVShow.user_id == current_user.id
    ).all()

    tv_data = {
        "watchlist": [],
        "watching": [],
        "completed": []
    }

    for utv, tv in tv_shows:
        tv_data[utv.status].append({
            "tmdb_tv_id": tv.tmdb_tv_id,
            "name": tv.name,
            "first_air_year": tv.first_air_year,
            "current_season": utv.current_season,
            "current_episode": utv.current_episode,
            "poster_path": tv.poster_path, 
        })

    return {
        "movies": movies_data,
        "tv": tv_data
    }
