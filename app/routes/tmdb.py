from fastapi import APIRouter, Query, HTTPException
from app.services.tmdb import tmdb_get

router = APIRouter(prefix="/tmdb", tags=["tmdb"])


# ---------- MOVIE SEARCH ----------
@router.get("/search/movie")
def search_movies(
    query: str = Query(..., min_length=1),
    year: int | None = None
):
    params = {
        "query": query,
        "include_adult": False,
    }

    if year:
        params["year"] = year

    data = tmdb_get("/search/movie", params)

    return {
        "results": [
            {
                "tmdb_movie_id": m["id"],
                "title": m.get("title"),
                "release_year": (
                    m.get("release_date", "")[:4]
                    if m.get("release_date") else None
                ),
                "poster_path": m.get("poster_path"),
            }
            for m in data.get("results", [])
        ]
    }


# ---------- MOVIE DETAILS ----------
@router.get("/movie/{tmdb_movie_id}")
def movie_details(tmdb_movie_id: int):
    data = tmdb_get(f"/movie/{tmdb_movie_id}")

    return {
        "tmdb_movie_id": data["id"],
        "title": data.get("title"),
        "overview": data.get("overview"),
        "release_year": (
            data.get("release_date", "")[:4]
            if data.get("release_date") else None
        ),
        "poster_path": data.get("poster_path"),
    }


# ---------- TV SEARCH ----------
@router.get("/search/tv")
def search_tv(
    query: str = Query(..., min_length=1)
):
    params = {
        "query": query,
        "include_adult": False,
    }

    data = tmdb_get("/search/tv", params)

    return {
        "results": [
            {
                "tmdb_tv_id": tv["id"],
                "name": tv.get("name"),
                "first_air_year": (
                    tv.get("first_air_date", "")[:4]
                    if tv.get("first_air_date") else None
                ),
                "poster_path": tv.get("poster_path"),
            }
            for tv in data.get("results", [])
        ]
    }


# ---------- TV DETAILS ----------
@router.get("/tv/{tmdb_tv_id}")
def tv_details(tmdb_tv_id: int):
    try:
        data = tmdb_get(f"/tv/{tmdb_tv_id}")
    except RuntimeError as e:
        print("TMDB TV DETAILS ERROR:", e)
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch TV details from TMDB"
        )

    return {
        "tmdb_tv_id": data["id"],
        "name": data.get("name"),
        "overview": data.get("overview"),
        "first_air_year": (
            data.get("first_air_date", "")[:4]
            if data.get("first_air_date") else None
        ),
        "number_of_seasons": data.get("number_of_seasons"),
        "poster_path": data.get("poster_path"),
    }