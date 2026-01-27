from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.auth.dependencies import get_current_user
from app.models.movie import Movie
from app.models.user_movie import UserMovie
from app.schemas.movie import MovieCreate

router = APIRouter(prefix="/movies", tags=["movies"])


@router.post("/save")
def save_movie(
    movie_in: MovieCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1. Check if movie exists
    movie = db.query(Movie).filter(
        Movie.tmdb_movie_id == movie_in.tmdb_movie_id
    ).first()

    if not movie:
        movie = Movie(
            tmdb_movie_id=movie_in.tmdb_movie_id,
            title=movie_in.title,
            release_year=movie_in.release_year,
            poster_path=movie_in.poster_path
        )
        db.add(movie)
        db.commit()
        db.refresh(movie)

    # 2. Check if user already saved this movie
    existing = db.query(UserMovie).filter(
        UserMovie.user_id == current_user.id,
        UserMovie.movie_id == movie.id
    ).first()

    if existing:
        existing.status = movie_in.status
        existing.poster_path = movie_in.poster_path

        db.commit()
        return {"message": "Movie updated successfully"}

    # 3. Save user-movie relation
    user_movie = UserMovie(
        user_id=current_user.id,
        movie_id=movie.id,
        status=movie_in.status,
    )
    db.add(user_movie)
    db.commit()

    return {"message": "Movie saved successfully"}

@router.delete("/{tmdb_movie_id}")
def remove_movie(
    tmdb_movie_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    movie = db.query(Movie).filter(
        Movie.tmdb_movie_id == tmdb_movie_id
    ).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    user_movie = db.query(UserMovie).filter(
        UserMovie.user_id == current_user.id,
        UserMovie.movie_id == movie.id
    ).first()

    if not user_movie:
        raise HTTPException(status_code=404, detail="Movie not in your list")

    db.delete(user_movie)
    db.commit()

    return {"message": "Movie removed"}