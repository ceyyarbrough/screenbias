# omdb.py
# Contains routes that interact with the OMDb API for the home page and movie galleries.

from . import app
from flask import render_template
import requests

# OMDb API key (should be stored securely in production)
OMDB_API_KEY = "16deab3b"

# Home page route: displays three movie galleries using OMDb API data
@app.route('/')
@app.route('/home')
def home():
    # Fetch newest movies (by year)
    newest_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s=2023&type=movie"
    newest_resp = requests.get(newest_url)
    newest_movies = newest_resp.json().get('Search', []) if newest_resp.status_code == 200 else []
    # Sort by year descending and take the 10 most recent
    try:
        newest_movies = sorted(newest_movies, key=lambda m: int(m.get('Year', 0)), reverse=True)[:10]
    except Exception:
        newest_movies = newest_movies[:10]

    # Fetch movies by actor (e.g., Tom Hanks)
    actor_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s=Tom%20Hanks&type=movie"
    actor_resp = requests.get(actor_url)
    actor_movies = actor_resp.json().get('Search', [])[:10] if actor_resp.status_code == 200 else []

    # Fetch movies by director (e.g., Christopher Nolan)
    director_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s=Christopher%20Nolan&type=movie"
    director_resp = requests.get(director_url)
    director_movies = director_resp.json().get('Search', [])[:10] if director_resp.status_code == 200 else []

    # Render the index.html template with all movie galleries
    return render_template(
        'index.html',
        name='screenbias',
        newest_movies=newest_movies,
        actor_movies=actor_movies,
        director_movies=director_movies
    )
