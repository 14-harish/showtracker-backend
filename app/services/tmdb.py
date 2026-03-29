from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Create a session with retry logic
def make_session():
    session = requests.Session()
    retry = Retry(
        total=3,              # retry 3 times
        backoff_factor=1,     # wait 1s, 2s, 4s between retries
        status_forcelist=[429, 500, 502, 503, 504],  # retry on these status codes
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

SESSION = make_session()

def tmdb_get(endpoint: str, params: dict | None = None):
    if not TMDB_API_KEY:
        raise RuntimeError("TMDB_API_KEY is not set")
    
    query = {"api_key": TMDB_API_KEY}
    if params:
        query.update(params)
    
    try:
        print(f"TMDB CALL → {endpoint}")
        response = SESSION.get(
            f"{TMDB_BASE_URL}{endpoint}",
            params=query,
            timeout=30,        # increased from 20
            verify=False,      # your working fix for now
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json",
            }
        )
        print("TMDB STATUS:", response.status_code)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        print("TMDB TIMEOUT")
        raise RuntimeError("TMDB timeout — try again")
    except requests.exceptions.ConnectionError as e:
        print("TMDB CONNECTION ERROR:", repr(e))
        raise RuntimeError("TMDB connection failed")
    except requests.exceptions.HTTPError:
        print("TMDB HTTP ERROR:", response.status_code, response.text)
        raise RuntimeError(f"TMDB error: {response.status_code}")
    except Exception as e:
        print("TMDB UNKNOWN ERROR:", repr(e))
        raise RuntimeError("TMDB unknown error")
