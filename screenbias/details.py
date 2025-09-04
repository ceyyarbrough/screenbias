# details.py
# Handles the route for displaying details of a specific movie (login required).

from . import app
from flask import render_template, session, redirect, url_for, flash, abort
import requests

# OMDb API key (should be stored securely in production)
OMDB_API_KEY = "SECRET KEY GOES HERE"

# Movie details route: shows details for a specific movie, requires login
@app.route('/details/<movie_id>', methods=['GET'])
def movie_details(movie_id):
    # Restrict access to reviews unless logged in
    if 'username' not in session:
        flash('You must be logged in to review movies.', 'warning')
        return redirect(url_for('login'))
    # Call the OMDb API to fetch movie details
    api_url = f"http://www.omdbapi.com/?i={movie_id}&apikey={OMDB_API_KEY}"
    response = requests.get(api_url)
    if response.status_code != 200 or not response.json().get('Response') == 'True':
        abort(404, description="Movie not found or API error")
    # Parse the JSON response
    movie = response.json()
    # Render the movie details template
    return render_template('movie_details.html', movie=movie)
