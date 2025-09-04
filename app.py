
# Import necessary modules from Flask and Python standard library
from flask import Flask, render_template, request, abort, redirect, url_for, session, flash  # Flask web framework
import requests  # For making HTTP requests to OMDb API
import os  # For accessing environment variables
from datetime import datetime  # For getting the current year

# Initialize Flask app
app = Flask(__name__)
# Secret key for session management (change in production)
app.secret_key = 'API Key Goes Here'

# Make the current year available in all templates
@app.context_processor
def inject_year():
    # Injects the current year as 'year' into all templates
    return {'year': datetime.now().year}

# OMDb API key (set as environment variable for security)
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

###########################################################
# --- Movies Routes ---
###########################################################

# Route for right wing movies page
@app.route('/movies/rightwing')
def movies_rightwing():
    return render_template('movies_rightwing.html')


# Route for left wing movies page
@app.route('/movies/leftwing')
def movies_leftwing():
    return render_template('movies_leftwing.html')


# Route for centrist movies page
@app.route('/movies/center')
def movies_center():
    return render_template('movies_center.html')

###########################################################
# --- TV Shows/Series Routes ---
###########################################################

# Route for right wing TV shows/series page
@app.route('/tv/rightwing')
def tv_rightwing():
    return render_template('tv_rightwing.html')


# Route for left wing TV shows/series page
@app.route('/tv/leftwing')
def tv_leftwing():
    return render_template('tv_leftwing.html')


# Route for centrist TV shows/series page
@app.route('/tv/center')
def tv_center():
    return render_template('tv_center.html')

###########################################################
# --- Actors Routes ---
###########################################################

# Route for right wing actors page
@app.route('/actors/rightwing')
def actors_rightwing():
    return render_template('actors_rightwing.html')


# Route for left wing actors page
@app.route('/actors/leftwing')
def actors_leftwing():
    return render_template('actors_leftwing.html')


# Route for centrist actors page
@app.route('/actors/center')
def actors_center():
    return render_template('actors_center.html')

###########################################################
# --- Directors Routes ---
###########################################################

# Route for right wing directors page
@app.route('/directors/rightwing')
def directors_rightwing():
    return render_template('directors_rightwing.html')


# Route for left wing directors page
@app.route('/directors/leftwing')
def directors_leftwing():
    return render_template('directors_leftwing.html')


# Route for centrist directors page
@app.route('/directors/center')
def directors_center():
    return render_template('directors_center.html')

###########################################################
# --- Stats Route ---
###########################################################

# Route for stats page
@app.route('/stats')
def stats():
    return render_template('stats.html')

###########################################################
# --- Home Page Route ---
###########################################################

# Route for the home page, displays 3 movie galleries using OMDb API data
@app.route('/')
@app.route('/home')
def home():
    # Fetch newest movies (by year)
    newest_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s=2023&type=movie"
    newest_resp = requests.get(newest_url)
    # Get up to 10 newest movies
    newest_movies = newest_resp.json().get('Search', [])[:10] if newest_resp.status_code == 200 else []

    # Fetch movies by actor (e.g., Tom Hanks)
    actor_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s=Tom%20Hanks&type=movie"
    actor_resp = requests.get(actor_url)
    # Get up to 10 movies for the actor
    actor_movies = actor_resp.json().get('Search', [])[:10] if actor_resp.status_code == 200 else []

    # Fetch movies by director (e.g., Christopher Nolan)
    director_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s=Christopher%20Nolan&type=movie"
    director_resp = requests.get(director_url)
    # Get up to 10 movies for the director
    director_movies = director_resp.json().get('Search', [])[:10] if director_resp.status_code == 200 else []

    # Render the index.html template with all movie galleries
    return render_template(
        'index.html',
        name='screenbias',
        newest_movies=newest_movies,
        actor_movies=actor_movies,
        director_movies=director_movies
    )


# Simple user store for demonstration (replace with a database in production)
USERS = {
    'chris': 'password1',
    'nicole': 'password2',
}

###########################################################
# --- Login Route ---
###########################################################

# Route for user login page and authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle user login
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Check credentials
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

###########################################################
# --- Logout Route ---
###########################################################

# Route for logging out the user
@app.route('/logout')
def logout():
    # Remove user from session
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

###########################################################
# --- Legacy Routes (for old pages) ---
###########################################################

# Route for legacy right wing films page
@app.route('/rightwing')
def rightwing():
    return render_template('right.html', name='rightscreenbias')


# Route for legacy left wing films page
@app.route('/leftwing')
def leftwing():
    return render_template('left.html', name='leftscreenbias')


# Route for legacy centrist films page
@app.route('/centerwing')
def centerwing():
    return render_template('center.html', name='centerscreenbias')

###########################################################
# --- Search Route ---
###########################################################

# Route for searching movies using OMDb API
@app.route('/search')
def search():
    # Get the search term from the query string
    query = request.args.get('query')
    if not query:
        return render_template('search_results.html', results=[], error="No query provided.")

    # Build OMDb API URL for search
    api_url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={query}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        results = response.json().get('Search', [])  # Extract the 'Search' key
    except requests.RequestException as e:
        return render_template('search_results.html', results=[], error=str(e))

    return render_template('search_results.html', results=results, error=None)

###########################################################
# --- Movie Details Route ---
###########################################################

# Route for displaying details of a specific movie
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
    return render_template('movie_details.html', movie=movie)


###########################################################
# --- Main entry point ---
###########################################################
# Run the Flask app
if __name__ == '__main__':
    app.run()