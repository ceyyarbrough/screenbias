# details.py
# Handles the route for displaying details of a specific movie (login required).


from . import app
from flask import render_template, session, redirect, url_for, flash, abort, request
import requests
from .models import db, Review

# OMDb API key (should be stored securely in production)
OMDB_API_KEY = "16deab3b"


# Movie details route: shows details for a specific movie, allows review if logged in
@app.route('/details/<movie_id>', methods=['GET', 'POST'])
def movie_details(movie_id):
    # Call the OMDb API to fetch movie details
    api_url = f"http://www.omdbapi.com/?i={movie_id}&apikey={OMDB_API_KEY}"
    response = requests.get(api_url)
    if response.status_code != 200 or not response.json().get('Response') == 'True':
        abort(404, description="Movie not found or API error")
    movie = response.json()

    # Handle review submission
    if request.method == 'POST':
        if 'username' not in session:
            flash('You must be logged in to review movies.', 'warning')
            return redirect(url_for('login'))
        rating = int(request.form.get('rating', 50))
        review_text = request.form.get('review_text', '').strip()
        if not review_text:
            flash('Review text is required.', 'danger')
        else:
            review = Review(movie_id=movie_id, username=session['username'], rating=rating, review_text=review_text)
            db.session.add(review)
            db.session.commit()
            flash('Your review has been submitted!', 'success')
            return redirect(url_for('movie_details', movie_id=movie_id))

    # Fetch all reviews for this movie
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    avg_rating = None
    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
    return render_template('movie_details.html', movie=movie, reviews=reviews, avg_rating=avg_rating)
