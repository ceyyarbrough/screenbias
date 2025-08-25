from flask import Flask, render_template, request, abort, redirect, url_for, session, flash
import requests
import os


# Initialize Flask app
app = Flask(__name__)
# Secret key for session management (change in production)
app.secret_key = 'your_secret_key_here'

# OMDb API key (set as environment variable for security)
OMDB_API_KEY = os.getenv('OMDB_API_KEY')



# --- Movies Routes ---
@app.route('/movies/rightwing')
def movies_rightwing():
    # Render right wing movies page
    return render_template('movies_rightwing.html')

@app.route('/movies/leftwing')
def movies_leftwing():
    # Render left wing movies page
    return render_template('movies_leftwing.html')

@app.route('/movies/center')
def movies_center():
    # Render centrist movies page
    return render_template('movies_center.html')


# --- TV Shows/Series Routes ---
@app.route('/tv/rightwing')
def tv_rightwing():
    # Render right wing TV shows/series page
    return render_template('tv_rightwing.html')

@app.route('/tv/leftwing')
def tv_leftwing():
    # Render left wing TV shows/series page
    return render_template('tv_leftwing.html')

@app.route('/tv/center')
def tv_center():
    # Render centrist TV shows/series page
    return render_template('tv_center.html')


# --- Actors Routes ---
@app.route('/actors/rightwing')
def actors_rightwing():
    # Render right wing actors page
    return render_template('actors_rightwing.html')

@app.route('/actors/leftwing')
def actors_leftwing():
    # Render left wing actors page
    return render_template('actors_leftwing.html')

@app.route('/actors/center')
def actors_center():
    # Render centrist actors page
    return render_template('actors_center.html')


# --- Directors Routes ---
@app.route('/directors/rightwing')
def directors_rightwing():
    # Render right wing directors page
    return render_template('directors_rightwing.html')

@app.route('/directors/leftwing')
def directors_leftwing():
    # Render left wing directors page
    return render_template('directors_leftwing.html')

@app.route('/directors/center')
def directors_center():
    # Render centrist directors page
    return render_template('directors_center.html')

 
# --- Stats Route ---
@app.route('/stats')
def stats():
    # Render stats page
    return render_template('stats.html')




# --- Home Page Route ---
@app.route('/')
@app.route('/home')
def home():
    # Render the home page
    return render_template('index.html', name='screenbias')



# Simple user store for demonstration (replace with a database in production)
USERS = {
    'chris': 'password1',
    'nicole': 'password2',
}


# --- Login Route ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle user login
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')


# --- Logout Route ---
@app.route('/logout')
def logout():
    # Handle user logout
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))


# --- Legacy Routes (for old pages) ---
@app.route('/rightwing')
def rightwing():
    # Render legacy right wing films page
    return render_template('right.html', name='rightscreenbias')

@app.route('/leftwing')
def leftwing():
    # Render legacy left wing films page
    return render_template('left.html', name='leftscreenbias')

@app.route('/centerwing')
def centerwing():
    # Render legacy centrist films page
    return render_template('center.html', name='centerscreenbias')


# --- Search Route ---
@app.route('/search')
def search():
    # Handle search queries and display results
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


# --- Movie Details Route ---
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


# --- Main entry point ---
if __name__ == '__main__':
    app.run()
