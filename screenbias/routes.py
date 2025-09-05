# routes.py
# Contains routes for static pages and main navigation (movies, TV, actors, directors, stats).


from . import app
from flask import render_template
from .models import Review
import requests
OMDB_API_KEY = "16deab3b"

# --- Movies Routes ---

# Helper to get OMDb movie details for a list of imdbIDs
def get_movies_by_ids_with_ratings(imdb_ids, ratings_dict):
    movies = []
    for imdb_id in imdb_ids:
        api_url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
        resp = requests.get(api_url)
        if resp.status_code == 200 and resp.json().get('Response') == 'True':
            movie = resp.json()
            movie['avg_rating'] = ratings_dict.get(imdb_id)
            movies.append(movie)
    # Sort by avg_rating descending
    movies.sort(key=lambda m: m.get('avg_rating', 0), reverse=True)
    return movies

@app.route('/movies/rightwing')
def movies_rightwing():
    # Get all reviews, group by movie, filter for avg_rating > 66
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    rightwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) > 66]
    rightwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in rightwing_ids}
    movies = get_movies_by_ids_with_ratings(rightwing_ids, rightwing_ratings)
    return render_template('movies_rightwing.html', movies=movies)

@app.route('/movies/leftwing')
def movies_leftwing():
    # Get all reviews, group by movie, filter for avg_rating < 33
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    leftwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) < 33]
    leftwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in leftwing_ids}
    movies = get_movies_by_ids_with_ratings(leftwing_ids, leftwing_ratings)
    return render_template('movies_leftwing.html', movies=movies)

@app.route('/movies/center')
def movies_center():
    # Get all reviews, group by movie, filter for 33 <= avg_rating <= 66
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    center_ids = [mid for mid, ratings in movie_reviews.items() if ratings and 33 <= (sum(ratings)/len(ratings)) <= 66]
    center_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in center_ids}
    movies = get_movies_by_ids_with_ratings(center_ids, center_ratings)
    return render_template('movies_center.html', movies=movies)


# TV Shows/Series Routes (by leaning, using review system)
def get_tv_by_ids_with_ratings(imdb_ids, ratings_dict):
    shows = []
    for imdb_id in imdb_ids:
        api_url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
        resp = requests.get(api_url)
        if resp.status_code == 200 and resp.json().get('Response') == 'True' and resp.json().get('Type') == 'series':
            show = resp.json()
            show['avg_rating'] = ratings_dict.get(imdb_id)
            shows.append(show)
    shows.sort(key=lambda s: s.get('avg_rating', 0), reverse=True)
    return shows

@app.route('/tv/rightwing')
def tv_rightwing():
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    rightwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) > 66]
    rightwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in rightwing_ids}
    shows = get_tv_by_ids_with_ratings(rightwing_ids, rightwing_ratings)
    return render_template('tv_rightwing.html', shows=shows)

@app.route('/tv/leftwing')
def tv_leftwing():
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    leftwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) < 33]
    leftwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in leftwing_ids}
    shows = get_tv_by_ids_with_ratings(leftwing_ids, leftwing_ratings)
    return render_template('tv_leftwing.html', shows=shows)

@app.route('/tv/center')
def tv_center():
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    center_ids = [mid for mid, ratings in movie_reviews.items() if ratings and 33 <= (sum(ratings)/len(ratings)) <= 66]
    center_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in center_ids}
    shows = get_tv_by_ids_with_ratings(center_ids, center_ratings)
    return render_template('tv_center.html', shows=shows)


# Actors Routes (by leaning, using review system)
def get_actors_by_ids_with_ratings(imdb_ids, ratings_dict):
    # For demo, treat as movies for now (OMDb does not provide actor details by imdbID)
    actors = []
    for imdb_id in imdb_ids:
        api_url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
        resp = requests.get(api_url)
        if resp.status_code == 200 and resp.json().get('Response') == 'True':
            actor = resp.json()
            actor['avg_rating'] = ratings_dict.get(imdb_id)
            actors.append(actor)
    actors.sort(key=lambda a: a.get('avg_rating', 0), reverse=True)
    return actors

@app.route('/actors/rightwing')
def actors_rightwing():
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    rightwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) > 66]
    rightwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in rightwing_ids}
    actors = get_actors_by_ids_with_ratings(rightwing_ids, rightwing_ratings)
    return render_template('actors_rightwing.html', actors=actors)

@app.route('/actors/leftwing')
def actors_leftwing():
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    leftwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) < 33]
    leftwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in leftwing_ids}
    actors = get_actors_by_ids_with_ratings(leftwing_ids, leftwing_ratings)
    return render_template('actors_leftwing.html', actors=actors)

@app.route('/actors/center')
def actors_center():
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    center_ids = [mid for mid, ratings in movie_reviews.items() if ratings and 33 <= (sum(ratings)/len(ratings)) <= 66]
    center_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in center_ids}
    actors = get_actors_by_ids_with_ratings(center_ids, center_ratings)
    return render_template('actors_center.html', actors=actors)


# Directors Routes (by leaning, using review system)
def get_directors_by_ids_with_ratings(imdb_ids, ratings_dict):
    # For demo, treat as movies for now (OMDb does not provide director details by imdbID)
    directors = []
    for imdb_id in imdb_ids:
        api_url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
        resp = requests.get(api_url)
        if resp.status_code == 200 and resp.json().get('Response') == 'True':
            director = resp.json()
            director['avg_rating'] = ratings_dict.get(imdb_id)
            directors.append(director)
    directors.sort(key=lambda d: d.get('avg_rating', 0), reverse=True)
    return directors

@app.route('/directors/rightwing')
def directors_rightwing():
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    rightwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) > 66]
    rightwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in rightwing_ids}
    directors = get_directors_by_ids_with_ratings(rightwing_ids, rightwing_ratings)
    return render_template('directors_rightwing.html', directors=directors)

@app.route('/directors/leftwing')
def directors_leftwing():
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    leftwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) < 33]
    leftwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in leftwing_ids}
    directors = get_directors_by_ids_with_ratings(leftwing_ids, leftwing_ratings)
    return render_template('directors_leftwing.html', directors=directors)

@app.route('/directors/center')
def directors_center():
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    center_ids = [mid for mid, ratings in movie_reviews.items() if ratings and 33 <= (sum(ratings)/len(ratings)) <= 66]
    center_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in center_ids}
    directors = get_directors_by_ids_with_ratings(center_ids, center_ratings)
    return render_template('directors_center.html', directors=directors)

# --- Stats Route ---
@app.route('/stats')
def stats():
    """Render the stats page."""
    return render_template('stats.html')

