
# search.py
# Handles the search route for querying movies using the OMDb API.

from . import app
from flask import render_template, request
import requests



# OMDb API key (should be stored securely in production)
import os
OMDB_API_KEY = os.environ.get('OMDB_API_KEY', 'insecure-demo-key')
if OMDB_API_KEY == 'insecure-demo-key':
    import warnings
    warnings.warn('WARNING: Using insecure default OMDb API key! Set OMDB_API_KEY in your environment for production.')


# Search route: queries OMDb API for movies matching the search term
@app.route('/search')
def search():
    """
    Search page. Queries OMDb API for movies matching the search term from the query string.
    Displays results or error message in search_results.html.
    """
    # Get the search term from the query string
    query = request.args.get('query')
    if not query:
        return render_template('search_results.html', results=[], error="No query provided.")

    # Build OMDb API URL for search
    api_url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={query}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        results = response.json().get('Search', [])
    except requests.RequestException as e:
        return render_template('search_results.html', results=[], error=str(e))
    # Render the search results template
    return render_template('search_results.html', results=results, error=None)
