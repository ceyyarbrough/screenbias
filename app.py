from flask import Flask, render_template, request, abort, redirect, url_for, session, flash
import requests
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production

OMDB_API_KEY = os.getenv('OMDB_API_KEY')


# Movies
@app.route('/movies/rightwing')
def movies_rightwing():
    return render_template('movies_rightwing.html')

@app.route('/movies/leftwing')
def movies_leftwing():
    return render_template('movies_leftwing.html')

@app.route('/movies/center')
def movies_center():
    return render_template('movies_center.html')

# TV Shows/Series
@app.route('/tv/rightwing')
def tv_rightwing():
    return render_template('tv_rightwing.html')

@app.route('/tv/leftwing')
def tv_leftwing():
    return render_template('tv_leftwing.html')

@app.route('/tv/center')
def tv_center():
    return render_template('tv_center.html')

# Actors
@app.route('/actors/rightwing')
def actors_rightwing():
    return render_template('actors_rightwing.html')

@app.route('/actors/leftwing')
def actors_leftwing():
    return render_template('actors_leftwing.html')

@app.route('/actors/center')
def actors_center():
    return render_template('actors_center.html')

# Directors
@app.route('/directors/rightwing')
def directors_rightwing():
    return render_template('directors_rightwing.html')

@app.route('/directors/leftwing')
def directors_leftwing():
    return render_template('directors_leftwing.html')

@app.route('/directors/center')
def directors_center():
    return render_template('directors_center.html')

# Stats
@app.route('/stats')
def stats():
    return render_template('stats.html')
from flask import Flask, render_template, request, abort, redirect, url_for, session, flash
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production

OMDB_API_KEY = '16deab3b'


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', name='screenbias')


# Simple user store for demonstration
USERS = {
    'chris': 'password1',
    'nicole': 'password2',
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('hello_world'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/rightwing')
def rightwing():
    return render_template('right.html', name='rightscreenbias')

@app.route('/leftwing')
def leftwing():
    return render_template('left.html', name='leftscreenbias')

@app.route('/centerwing')
def centerwing():
    return render_template('center.html', name='centerscreenbias')

@app.route('/search')
def search():
    query = request.args.get('query')  # Get the search term from the query string
    if not query:
        return render_template('search_results.html', results=[], error="No query provided.")

    # Example API call (replace with your actual API endpoint and key)
    api_url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={query}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        results = response.json().get('Search', [])  # Extract the 'Search' key
    except requests.RequestException as e:
        return render_template('search_results.html', results=[], error=str(e))

    return render_template('search_results.html', results=results, error=None)

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
    movie = response.json()  # Parse the JSON response
    return render_template('movie_details.html', movie=movie)

if __name__ == '__main__':
    app.run()
