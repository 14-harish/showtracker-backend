from fastapi import APIRouter, Query, HTTPException
from app.services.tmdb import tmdb_get

router = APIRouter(prefix="/tmdb", tags=["tmdb"])


# ---------- HELPER FUNCTIONS ----------
def _extract_genres(raw_genres):
    return [
        {"id": g.get("id"), "name": g.get("name")}
        for g in (raw_genres or [])
        if isinstance(g, dict)
    ]


def _extract_cast(credits_data, limit=8):
    cast_list = credits_data.get("cast", []) if isinstance(credits_data, dict) else []
    return [
        {
            "id": c.get("id"),
            "name": c.get("name"),
            "character": c.get("character"),
            "profile_path": c.get("profile_path"),
        }
        for c in cast_list[:limit]
    ]


def _extract_single_trailer(videos_data):
    results = videos_data.get("results", []) if isinstance(videos_data, dict) else []
    yt_videos = [v for v in results if isinstance(v, dict) and v.get("site") == "YouTube"]
    if not yt_videos:
        return None

    # Priority 1: Official Trailer
    for v in yt_videos:
        if v.get("type") == "Trailer" and v.get("official") is True:
            return {"key": v.get("key"), "name": v.get("name"), "site": "YouTube"}

    # Priority 2: Official Teaser
    for v in yt_videos:
        if v.get("type") == "Teaser" and v.get("official") is True:
            return {"key": v.get("key"), "name": v.get("name"), "site": "YouTube"}

    # Priority 3: Trailer (any)
    for v in yt_videos:
        if v.get("type") == "Trailer":
            return {"key": v.get("key"), "name": v.get("name"), "site": "YouTube"}

    # Priority 4: First available YouTube video
    first = yt_videos[0]
    return {"key": first.get("key"), "name": first.get("name"), "site": "YouTube"}


def _extract_similar(similar_data, media_type, limit=12):
    results = similar_data.get("results", []) if isinstance(similar_data, dict) else []
    return [
        {
            "id": s.get("id"),
            "title": s.get("title") or s.get("name"),
            "poster_path": s.get("poster_path"),
            "media_type": media_type,
            "vote_average": round(s.get("vote_average", 0), 1) if s.get("vote_average") else 0,
            "release_year": (s.get("release_date") or s.get("first_air_date") or "")[:4],
        }
        for s in results[:limit]
    ]


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
    try:
        data = tmdb_get(
            f"/movie/{tmdb_movie_id}",
            params={"append_to_response": "credits,videos,similar"}
        )
    except RuntimeError as e:
        print("TMDB MOVIE DETAILS ERROR:", e)
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch movie details from TMDB"
        )

    credits_data = data.get("credits", {})
    crew_list = credits_data.get("crew", []) if isinstance(credits_data, dict) else []
    directors = [
        {"name": c.get("name"), "job": "Director"}
        for c in crew_list
        if c.get("job") == "Director"
    ]

    release_date = data.get("release_date") or ""

    return {
        "details": {
            "tmdb_id": data["id"],
            "media_type": "movie",
            "title": data.get("title"),
            "poster_path": data.get("poster_path"),
            "backdrop_path": data.get("backdrop_path"),
            "tagline": data.get("tagline"),
            "overview": data.get("overview"),
            "release_date": release_date,
            "release_year": release_date[:4] if release_date else None,
            "runtime": data.get("runtime"),
            "genres": _extract_genres(data.get("genres")),
            "original_language": (data.get("original_language") or "").upper(),
            "vote_average": round(data.get("vote_average", 0), 1) if data.get("vote_average") else 0,
            "vote_count": data.get("vote_count", 0),
            "status": data.get("status"),
        },
        "cast": _extract_cast(credits_data),
        "crew": directors,
        "trailer": _extract_single_trailer(data.get("videos")),
        "similar": _extract_similar(data.get("similar"), "movie"),
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
        data = tmdb_get(
            f"/tv/{tmdb_tv_id}",
            params={"append_to_response": "credits,videos,similar"}
        )
    except RuntimeError as e:
        print("TMDB TV DETAILS ERROR:", e)
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch TV details from TMDB"
        )

    # Crew: Creator(s)
    created_by = data.get("created_by", [])
    creators = [
        {"name": c.get("name"), "job": "Creator"}
        for c in created_by
        if isinstance(c, dict) and c.get("name")
    ]
    if not creators:
        credits_data = data.get("credits", {})
        crew_list = credits_data.get("crew", []) if isinstance(credits_data, dict) else []
        creators = [
            {"name": c.get("name"), "job": c.get("job") or "Creator"}
            for c in crew_list
            if c.get("job") in ["Creator", "Executive Producer", "Director"]
        ][:2]

    first_air_date = data.get("first_air_date") or ""

    # TV Runtime: first value from episode_run_time if available, else null
    ep_run_time = data.get("episode_run_time", [])
    runtime = ep_run_time[0] if (isinstance(ep_run_time, list) and len(ep_run_time) > 0) else None

    return {
        "details": {
            "tmdb_id": data["id"],
            "media_type": "tv",
            "title": data.get("name"),
            "poster_path": data.get("poster_path"),
            "backdrop_path": data.get("backdrop_path"),
            "tagline": data.get("tagline"),
            "overview": data.get("overview"),
            "release_date": first_air_date,
            "release_year": first_air_date[:4] if first_air_date else None,
            "runtime": runtime,
            "genres": _extract_genres(data.get("genres")),
            "original_language": (data.get("original_language") or "").upper(),
            "vote_average": round(data.get("vote_average", 0), 1) if data.get("vote_average") else 0,
            "vote_count": data.get("vote_count", 0),
            "status": data.get("status"),
        },
        "cast": _extract_cast(data.get("credits")),
        "crew": creators,
        "trailer": _extract_single_trailer(data.get("videos")),
        "similar": _extract_similar(data.get("similar"), "tv"),
    }