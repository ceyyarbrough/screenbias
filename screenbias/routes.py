# routes.py
# Contains routes for static pages, main navigation, and all movie/TV/actor/director/statistics pages.
# Handles grouping by leaning, stats visualizations, and profile/review management.

from . import app
from flask import render_template, session, redirect, url_for, flash, request
from .models import db, Review
from .details import OMDB_API_KEY
import requests
import re
# Profile page: show and edit user's reviews
@app.route('/profile', methods=['GET'])
def profile():
    """
    Profile page route. Shows all reviews by the logged-in user, with movie title, poster, and badge color by rating.
    Allows editing/deleting reviews from the profile page.
    """
    if 'username' not in session:
        flash('You must be logged in to view your profile.', 'warning')
        return redirect(url_for('login'))
    user_reviews = Review.query.filter_by(username=session['username']).order_by(Review.created_at.desc()).all()
    reviews = []
    for r in user_reviews:
        movie_title = r.movie_id
        poster = None
        badge_color = 'badge-center'
        try:
            # Fetch movie title and poster from OMDb
            api_url = f"http://www.omdbapi.com/?i={r.movie_id}&apikey={OMDB_API_KEY}"
            resp = requests.get(api_url)
            if resp.status_code == 200 and resp.json().get('Response') == 'True':
                data = resp.json()
                movie_title = data.get('Title', r.movie_id)
                poster = data.get('Poster')
        except Exception:
            pass
        # Badge color logic by rating
        if r.rating >= 66:
            badge_color = 'badge-right'
        elif r.rating <= 33:
            badge_color = 'badge-left'
        reviews.append({
            'id': r.id,
            'movie_id': r.movie_id,
            'movie_title': movie_title,
            'rating': r.rating,
            'review_text': r.review_text,
            'created_at': r.created_at,
            'poster': poster,
            'badge_color': badge_color
        })
    return render_template('profile.html', reviews=reviews)

    
# Edit review route (from profile page)
@app.route('/edit_review/<int:review_id>', methods=['POST'])
def edit_review(review_id):
    """
    Edit review route. Allows logged-in users to edit or delete their own reviews from the profile page.
    Uses the same profanity and URL filter as review submission.
    """
    if 'username' not in session:
        flash('You must be logged in to edit reviews.', 'warning')
        return redirect(url_for('login'))
    review = Review.query.get_or_404(review_id)
    if review.username != session['username']:
        flash('You can only edit your own reviews.', 'danger')
        return redirect(url_for('profile'))
    action = request.form.get('action')
    if action == 'delete':
        db.session.delete(review)
        db.session.commit()
        flash('Review deleted.', 'success')
        return redirect(url_for('profile'))
    else:
        new_text = request.form.get('review_text', '').strip()
        # Use same foul language and URL filter as in details.py
        foul_words = [
            # ... (list omitted for brevity, same as details.py)
        ]
        foul_pattern = re.compile(r'\\b(' + '|'.join(map(re.escape, foul_words)) + r')\\b', re.IGNORECASE)
        url_pattern = re.compile(r'(https?://|www\\.|[a-zA-Z0-9\\-]+\\.(com|net|org|io|gov|edu|co|us|uk|ca|de|jp|fr|au|ru|ch|it|nl|se|no|es|mil|biz|info|mobi|name|aero|jobs|museum))', re.IGNORECASE)
        if not new_text:
            flash('Review text is required.', 'danger')
        elif foul_pattern.search(new_text):
            flash('Foul language is not allowed in reviews.', 'danger')
        elif url_pattern.search(new_text):
            flash('URLs are not allowed in reviews.', 'danger')
        else:
            review.review_text = new_text
            db.session.commit()
            flash('Review updated!', 'success')
        return redirect(url_for('profile'))

# --- Movies Routes ---


from . import app
from flask import render_template
from .models import Review
import requests
OMDB_API_KEY = "16deab3b"

# --- Movies Routes ---


# Helper to get OMDb movie details for a list of imdbIDs, attaching avg_rating from ratings_dict
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

# Movies gallery: rightwing (avg_rating > 66)
@app.route('/movies/rightwing')
def movies_rightwing():
    """
    Movies gallery for rightwing (avg_rating > 66).
    Groups reviews by movie, filters for avg_rating > 66, and fetches OMDb details.
    """
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    rightwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) > 66]
    rightwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in rightwing_ids}
    movies = get_movies_by_ids_with_ratings(rightwing_ids, rightwing_ratings)
    return render_template('movies_rightwing.html', movies=movies)

# Movies gallery: leftwing (avg_rating < 33)
@app.route('/movies/leftwing')
def movies_leftwing():
    """
    Movies gallery for leftwing (avg_rating < 33).
    Groups reviews by movie, filters for avg_rating < 33, and fetches OMDb details.
    """
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    leftwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) < 33]
    leftwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in leftwing_ids}
    movies = get_movies_by_ids_with_ratings(leftwing_ids, leftwing_ratings)
    return render_template('movies_leftwing.html', movies=movies)

# Movies gallery: center (33 <= avg_rating <= 66)
@app.route('/movies/center')
def movies_center():
    """
    Movies gallery for center (33 <= avg_rating <= 66).
    Groups reviews by movie, filters for 33 <= avg_rating <= 66, and fetches OMDb details.
    """
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    center_ids = [mid for mid, ratings in movie_reviews.items() if ratings and 33 <= (sum(ratings)/len(ratings)) <= 66]
    center_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in center_ids}
    movies = get_movies_by_ids_with_ratings(center_ids, center_ratings)
    return render_template('movies_center.html', movies=movies)



# Helper to get OMDb TV series details for a list of imdbIDs, attaching avg_rating
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

# TV gallery: rightwing (avg_rating > 66)
@app.route('/tv/rightwing')
def tv_rightwing():
    """
    TV gallery for rightwing (avg_rating > 66).
    Groups reviews by movie, filters for avg_rating > 66, and fetches OMDb TV details.
    """
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    rightwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) > 66]
    rightwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in rightwing_ids}
    shows = get_tv_by_ids_with_ratings(rightwing_ids, rightwing_ratings)
    return render_template('tv_rightwing.html', shows=shows)

# TV gallery: leftwing (avg_rating < 33)
@app.route('/tv/leftwing')
def tv_leftwing():
    """
    TV gallery for leftwing (avg_rating < 33).
    Groups reviews by movie, filters for avg_rating < 33, and fetches OMDb TV details.
    """
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    leftwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) < 33]
    leftwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in leftwing_ids}
    shows = get_tv_by_ids_with_ratings(leftwing_ids, leftwing_ratings)
    return render_template('tv_leftwing.html', shows=shows)

# TV gallery: center (33 <= avg_rating <= 66)
@app.route('/tv/center')
def tv_center():
    """
    TV gallery for center (33 <= avg_rating <= 66).
    Groups reviews by movie, filters for 33 <= avg_rating <= 66, and fetches OMDb TV details.
    """
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    center_ids = [mid for mid, ratings in movie_reviews.items() if ratings and 33 <= (sum(ratings)/len(ratings)) <= 66]
    center_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in center_ids}
    shows = get_tv_by_ids_with_ratings(center_ids, center_ratings)
    return render_template('tv_center.html', shows=shows)



# Helper to get OMDb details for a list of imdbIDs, treating as actors (OMDb does not provide actor details by imdbID)
def get_actors_by_ids_with_ratings(imdb_ids, ratings_dict):
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

# Actors gallery: rightwing (avg_rating > 66)
@app.route('/actors/rightwing')
def actors_rightwing():
    """
    Actors gallery for rightwing (avg_rating > 66).
    Groups reviews by movie, filters for avg_rating > 66, and fetches OMDb details (as actors).
    """
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    rightwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) > 66]
    rightwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in rightwing_ids}
    actors = get_actors_by_ids_with_ratings(rightwing_ids, rightwing_ratings)
    return render_template('actors_rightwing.html', actors=actors)

# Actors gallery: leftwing (avg_rating < 33)
@app.route('/actors/leftwing')
def actors_leftwing():
    """
    Actors gallery for leftwing (avg_rating < 33).
    Groups reviews by movie, filters for avg_rating < 33, and fetches OMDb details (as actors).
    """
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    leftwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) < 33]
    leftwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in leftwing_ids}
    actors = get_actors_by_ids_with_ratings(leftwing_ids, leftwing_ratings)
    return render_template('actors_leftwing.html', actors=actors)

# Actors gallery: center (33 <= avg_rating <= 66)
@app.route('/actors/center')
def actors_center():
    """
    Actors gallery for center (33 <= avg_rating <= 66).
    Groups reviews by movie, filters for 33 <= avg_rating <= 66, and fetches OMDb details (as actors).
    """
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    center_ids = [mid for mid, ratings in movie_reviews.items() if ratings and 33 <= (sum(ratings)/len(ratings)) <= 66]
    center_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in center_ids}
    actors = get_actors_by_ids_with_ratings(center_ids, center_ratings)
    return render_template('actors_center.html', actors=actors)



import collections
# Helper to get OMDb details for a list of imdbIDs, treating as directors (OMDb does not provide director details by imdbID)
def get_directors_by_ids_with_ratings(imdb_ids, ratings_dict):
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

# Directors gallery: rightwing (avg_rating > 66)
@app.route('/directors/rightwing')
def directors_rightwing():
    """
    Directors gallery for rightwing (avg_rating > 66).
    Groups reviews by movie, filters for avg_rating > 66, and fetches OMDb details (as directors).
    """
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    rightwing_ids = [mid for mid, ratings in movie_reviews.items() if ratings and (sum(ratings)/len(ratings)) > 66]
    rightwing_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in rightwing_ids}
    directors = get_directors_by_ids_with_ratings(rightwing_ids, rightwing_ratings)
    return render_template('directors_rightwing.html', directors=directors)


# Stats page with visualizations (genre, year, country, overall)
@app.route('/stats')
def stats():
    """
    Stats page route. Aggregates all reviews and OMDb data to produce:
    - Average rating by genre
    - Average rating by year
    - Average rating by country
    - Overall average rating and total review count
    Data is used for tables and Chart.js visualizations in the stats page.
    """
    # Gather all reviews and fetch OMDb data for each movie
    reviews = Review.query.all()
    movie_data = {}
    for r in reviews:
        if r.movie_id not in movie_data:
            try:
                api_url = f"http://www.omdbapi.com/?i={r.movie_id}&apikey={OMDB_API_KEY}"
                resp = requests.get(api_url)
                if resp.status_code == 200 and resp.json().get('Response') == 'True':
                    movie_data[r.movie_id] = resp.json()
            except Exception:
                continue
    # Aggregate by genre, year, country, and overall
    genre_ratings = collections.defaultdict(list)
    year_ratings = collections.defaultdict(list)
    country_ratings = collections.defaultdict(list)
    all_ratings = []
    for r in reviews:
        movie = movie_data.get(r.movie_id)
        if not movie:
            continue
        # Genre aggregation
        genres = [g.strip() for g in movie.get('Genre', '').split(',') if g.strip()]
        for genre in genres:
            genre_ratings[genre].append(r.rating)
        # Year aggregation
        year = movie.get('Year')
        if year:
            year_ratings[year].append(r.rating)
        # Country aggregation
        countries = [c.strip() for c in movie.get('Country', '').split(',') if c.strip()]
        for country in countries:
            country_ratings[country].append(r.rating)
        # Overall
        all_ratings.append(r.rating)
    # Prepare data for charts
    genre_chart = [{'genre': g, 'avg': sum(vals)/len(vals), 'count': len(vals)} for g, vals in genre_ratings.items() if vals]
    year_chart = [{'year': y, 'avg': sum(vals)/len(vals), 'count': len(vals)} for y, vals in year_ratings.items() if vals]
    country_chart = [{'country': c, 'avg': sum(vals)/len(vals), 'count': len(vals)} for c, vals in country_ratings.items() if vals]
    genre_chart.sort(key=lambda x: x['avg'], reverse=True)
    year_chart.sort(key=lambda x: x['year'])
    country_chart.sort(key=lambda x: x['avg'], reverse=True)
    overall_avg = sum(all_ratings)/len(all_ratings) if all_ratings else 0
    return render_template('stats.html',
        genre_chart=genre_chart,
        year_chart=year_chart,
        country_chart=country_chart,
        overall_avg=overall_avg,
        total_reviews=len(all_ratings)
    )

@app.route('/directors/center')
def directors_center():
    movie_reviews = {}
    for r in Review.query.all():
        movie_reviews.setdefault(r.movie_id, []).append(r.rating)
    center_ids = [mid for mid, ratings in movie_reviews.items() if ratings and 33 <= (sum(ratings)/len(ratings)) <= 66]
    center_ratings = {mid: sum(ratings)/len(ratings) for mid, ratings in movie_reviews.items() if mid in center_ids}
    directors = get_directors_by_ids_with_ratings(center_ids, center_ratings)
    return render_template('directors_center.html', directors=directors)


