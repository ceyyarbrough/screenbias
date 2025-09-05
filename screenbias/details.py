
from flask import jsonify
from . import app
from flask import render_template, session, redirect, url_for, flash, abort, request
import requests
from .models import db, Review, ReviewReaction
import re

# details.py
# Handles the route for displaying details of a specific movie (login required).

@app.route('/review_reaction_counts/<int:review_id>')
def review_reaction_counts(review_id):
    up = ReviewReaction.query.filter_by(review_id=review_id, reaction='up').count()
    down = ReviewReaction.query.filter_by(review_id=review_id, reaction='down').count()
    return jsonify({'up': up, 'down': down})

@app.route('/review_reaction/<int:review_id>', methods=['POST'])
def review_reaction(review_id):
    if 'username' not in session:
        return jsonify({'error': 'Login required'}), 401
    data = request.get_json()
    reaction = data.get('reaction')
    if reaction not in ['up', 'down']:
        return jsonify({'error': 'Invalid reaction'}), 400
    # Only one reaction per user per review
    existing = ReviewReaction.query.filter_by(review_id=review_id, username=session['username']).first()
    if existing:
        if existing.reaction == reaction:
            db.session.delete(existing)
            db.session.commit()
            return jsonify({'status': 'removed'})
        else:
            existing.reaction = reaction
            db.session.commit()
            return jsonify({'status': 'updated'})
    else:
        new_reaction = ReviewReaction(review_id=review_id, username=session['username'], reaction=reaction)
        db.session.add(new_reaction)
        db.session.commit()
        return jsonify({'status': 'added'})

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
        # Prevent multiple reviews by the same user for the same movie
        existing_review = Review.query.filter_by(movie_id=movie_id, username=session['username']).first()
        if existing_review:
            flash('You have already reviewed this movie.', 'danger')
            return redirect(url_for('movie_details', movie_id=movie_id))
        rating = int(request.form.get('rating', 50))
        review_text = request.form.get('review_text', '').strip()
        foul_words = [
            'fuck', 'shit', 'bitch', 'asshole', 'bastard', 'dick', 'pussy', 'cunt', 'cock', 'fag', 'slut', 'whore', 'nigger', 'retard', 'faggot', 'motherfucker', 'twat', 'douche', 'crap', 'bollocks', 'wanker', 'prick', 'arse', 'bugger', 'damn', 'hell', 'suck', 'jerk', 'tit', 'cum', 'spunk', 'piss', 'shag', 'tosser', 'bollocks', 'arsehole', 'minge', 'knob', 'bellend', 'git', 'twat', 'shite', 'bollocks', 'arse', 'wank', 'shithead', 'shitface', 'douchebag', 'dipshit', 'dickhead', 'dildo', 'jackass', 'piss off', 'sod off', 'son of a bitch', 'bastard', 'bollocks', 'bugger', 'bloody', 'bollocks', 'arse', 'wanker', 'prat', 'git', 'twat', 'shag', 'tosser', 'knob', 'bellend', 'minge', 'pillock', 'plonker', 'numpty', 'muppet', 'berk', 'div', 'nonce', 'slag', 'skank', 'scrubber', 'tart', 'tramp', 'trollop', 'slapper', 'slag', 'sket', 'gash', 'gimp', 'goon', 'mong', 'minger', 'munter', 'nob', 'nonce', 'numpty', 'pillock', 'plonker', 'prat', 'scrubber', 'shag', 'skank', 'slag', 'slapper', 'slut', 'spaz', 'spunk', 'tart', 'tosser', 'tramp', 'trollop', 'twat', 'wank', 'wanker', 'whore', 'wuss'
        ]
        foul_pattern = re.compile(r'\\b(' + '|'.join(map(re.escape, foul_words)) + r')\\b', re.IGNORECASE)
        url_pattern = re.compile(r'(https?://|www\\.|[a-zA-Z0-9\\-]+\\.(com|net|org|io|gov|edu|co|us|uk|ca|de|jp|fr|au|ru|ch|it|nl|se|no|es|mil|biz|info|mobi|name|aero|jobs|museum))', re.IGNORECASE)
        if not review_text:
            flash('Review text is required.', 'danger')
        elif foul_pattern.search(review_text):
            flash('Foul language is not allowed in reviews.', 'danger')
        elif url_pattern.search(review_text):
            flash('URLs are not allowed in reviews.', 'danger')
        else:
            review = Review(movie_id=movie_id, username=session['username'], rating=rating, review_text=review_text)
            db.session.add(review)
            db.session.commit()
            flash('Your review has been submitted!', 'success')
            return redirect(url_for('movie_details', movie_id=movie_id))

    # Fetch all reviews for this movie
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    # Attach up/down counts to each review
    from .models import ReviewReaction
    for r in reviews:
        r.up_count = ReviewReaction.query.filter_by(review_id=r.id, reaction='up').count()
        r.down_count = ReviewReaction.query.filter_by(review_id=r.id, reaction='down').count()
    avg_rating = None
    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
    return render_template('movie_details.html', movie=movie, reviews=reviews, avg_rating=avg_rating)
