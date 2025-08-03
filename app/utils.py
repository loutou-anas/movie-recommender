import re
import os
from dotenv import load_dotenv
from tmdbv3api import TMDb, Movie

# Load API key from .env
load_dotenv()
tmdb_api_key = os.getenv("TMDB_API_KEY")

tmdb = TMDb()
tmdb.api_key = tmdb_api_key
tmdb.language = 'en'
tmdb.debug = False

movie_api = Movie()

def clean_title(title):
    """
    Convert "Godfather, The (1972)" -> "The Godfather"
    """
    title = re.sub(r'\(\d{4}\)', '', title).strip()
    if ',' in title:
        parts = title.split(', ')
        if len(parts) == 2:
            title = f"{parts[1]} {parts[0]}"
    return title.strip()

def fetch_poster_url(title):
    """
    Fetch poster from TMDB. Fallback to placeholder if not found.
    """
    try:
        search_title = clean_title(title)
        results = movie_api.search(search_title)
        if results and results[0].poster_path:
            return f"https://image.tmdb.org/t/p/w500{results[0].poster_path}"
    except Exception as e:
        print(f"[ERROR] TMDB poster fetch failed: {e}")
    return "https://via.placeholder.com/150x220.png?text=No+Poster"
