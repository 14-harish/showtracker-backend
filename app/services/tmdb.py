import os
import httpx

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"


def tmdb_get(endpoint: str, params: dict | None = None):
    if not TMDB_API_KEY:
        raise RuntimeError("TMDB_API_KEY is not set")

    query = {
        "api_key": TMDB_API_KEY
    }

    if params:
        query.update(params)

    try:
        response = httpx.get(
            f"{TMDB_BASE_URL}{endpoint}",
            params=query,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    except httpx.ConnectError:
        raise RuntimeError("TMDB connection failed")

    except httpx.HTTPStatusError as e:
        print("TMDB ERROR:", e.response.status_code, e.response.text)
        raise RuntimeError("TMDB request failed")