# routes.py
# Contains routes for static pages and main navigation (movies, TV, actors, directors, stats).

from . import app
from flask import render_template

# --- Movies Routes ---
@app.route('/movies/rightwing')
def movies_rightwing():
    """Render the right-wing movies page."""
    return render_template('movies_rightwing.html')

@app.route('/movies/leftwing')
def movies_leftwing():
    """Render the left-wing movies page."""
    return render_template('movies_leftwing.html')

@app.route('/movies/center')
def movies_center():
    """Render the center movies page."""
    return render_template('movies_center.html')

# --- TV Shows/Series Routes ---
@app.route('/tv/rightwing')
def tv_rightwing():
    """Render the right-wing TV shows page."""
    return render_template('tv_rightwing.html')

@app.route('/tv/leftwing')
def tv_leftwing():
    """Render the left-wing TV shows page."""
    return render_template('tv_leftwing.html')

@app.route('/tv/center')
def tv_center():
    """Render the center TV shows page."""
    return render_template('tv_center.html')

# --- Actors Routes ---
@app.route('/actors/rightwing')
def actors_rightwing():
    """Render the right-wing actors page."""
    return render_template('actors_rightwing.html')

@app.route('/actors/leftwing')
def actors_leftwing():
    """Render the left-wing actors page."""
    return render_template('actors_leftwing.html')

@app.route('/actors/center')
def actors_center():
    """Render the center actors page."""
    return render_template('actors_center.html')

# --- Directors Routes ---
@app.route('/directors/rightwing')
def directors_rightwing():
    """Render the right-wing directors page."""
    return render_template('directors_rightwing.html')

@app.route('/directors/leftwing')
def directors_leftwing():
    """Render the left-wing directors page."""
    return render_template('directors_leftwing.html')

@app.route('/directors/center')
def directors_center():
    """Render the center directors page."""
    return render_template('directors_center.html')

# --- Stats Route ---
@app.route('/stats')
def stats():
    """Render the stats page."""
    return render_template('stats.html')

