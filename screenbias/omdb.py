
# omdb.py
# Contains routes that interact with the OMDb API for the home page and movie galleries.
# Handles fetching and displaying movie galleries (newest, recently reviewed, most reviewed, by actor, by director).



from . import app
from flask import render_template
import requests
from .models import Review



# OMDb API key (should be stored securely in production)
import os
OMDB_API_KEY = os.environ.get('OMDB_API_KEY', 'insecure-demo-key')
if OMDB_API_KEY == 'insecure-demo-key':
    import warnings
    warnings.warn('WARNING: Using insecure default OMDb API key! Set OMDB_API_KEY in your environment for production.')


# Home page route: displays movie galleries using OMDb API data
@app.route('/')
@app.route('/home')
def home():
    """
    Home page route. Displays:
    - Newest movies (2025 only, using multiple search terms to maximize OMDb results)
    - Movies by actor (Tom Hanks)
    - Movies by director (Christopher Nolan)
    - Recently reviewed movies (last 10 unique movies with reviews, includes avg_rating)
    - Most reviewed movies (top 10 by number of reviews, includes avg_rating and review_count)
    """
    # Fetch newest movies (2025 only) - OMDb API requires a more specific search term
    search_terms = ['the', 'a', 'of', 'in', 'on', 'and', 'to', 'for', 'with', 'by']
    seen_ids = set()
    newest_movies = []
    for term in search_terms:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&y=2025&type=movie&s={term}"
        resp = requests.get(url)
        if resp.status_code == 200:
            # OMDb returns up to 10 results per search term
            results = resp.json().get('Search', [])
            for m in results:
                # Only add unique 2025 movies
                if m.get('Year') == '2025' and m.get('imdbID') not in seen_ids:
                    newest_movies.append(m)
                    seen_ids.add(m.get('imdbID'))
                if len(newest_movies) >= 10:
                    break
        if len(newest_movies) >= 10:
            break

    # Fetch movies by actor (e.g., Tom Hanks)
    actor_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s=Tom%20Hanks&type=movie"
    actor_resp = requests.get(actor_url)
    actor_movies = actor_resp.json().get('Search', [])[:10] if actor_resp.status_code == 200 else []

    # Fetch movies by director (e.g., Christopher Nolan)
    director_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s=Christopher%20Nolan&type=movie"
    director_resp = requests.get(director_url)
    director_movies = director_resp.json().get('Search', [])[:10] if director_resp.status_code == 200 else []

    # Recently reviewed movies (last 10 reviews, unique movies)
    recent_reviews = Review.query.order_by(Review.created_at.desc()).all()
    seen = set()
    recent_movie_ids = []
    for r in recent_reviews:
        if r.movie_id not in seen:
            seen.add(r.movie_id)
            recent_movie_ids.append(r.movie_id)
        if len(recent_movie_ids) >= 10:
            break

    # Attach avg_rating to each recently reviewed movie
    recently_reviewed = []
    from .models import db
    for imdb_id in recent_movie_ids:
        api_url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
        resp = requests.get(api_url)
        if resp.status_code == 200 and resp.json().get('Response') == 'True':
            movie = resp.json()
            # Calculate average rating for this movie
            reviews = Review.query.filter_by(movie_id=imdb_id).all()
            if reviews:
                avg_rating = sum(r.rating for r in reviews) / len(reviews)
                movie['avg_rating'] = avg_rating
            else:
                movie['avg_rating'] = None
            recently_reviewed.append(movie)

    # Most reviewed movies (top 10 by number of reviews)
    from collections import Counter
    review_counts = Counter([r.movie_id for r in Review.query.all()])
    most_reviewed_ids = [imdb_id for imdb_id, count in review_counts.most_common(10)]
    most_reviewed = []
    for imdb_id in most_reviewed_ids:
        api_url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
        resp = requests.get(api_url)
        if resp.status_code == 200 and resp.json().get('Response') == 'True':
            movie = resp.json()
            movie['review_count'] = review_counts[imdb_id]
            # Calculate avg_rating for this movie
            reviews = Review.query.filter_by(movie_id=imdb_id).all()
            if reviews:
                avg_rating = sum(r.rating for r in reviews) / len(reviews)
                movie['avg_rating'] = avg_rating
            else:
                movie['avg_rating'] = None
            most_reviewed.append(movie)

    # Render the index.html template with all movie galleries
    return render_template(
        'index.html',
        name='screenbias',
        newest_movies=newest_movies,
        actor_movies=actor_movies,
        director_movies=director_movies,
        recently_reviewed=recently_reviewed,
        most_reviewed=most_reviewed
    )
