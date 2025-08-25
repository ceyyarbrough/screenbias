from flask import Flask, render_template, request, abort
import requests
import os

app = Flask(__name__)

OMDB_API_KEY = os.getenv('OMDB_API_KEY')

@app.route('/')
@app.route('/home')
def hello_world():
    return render_template('index.html', name='screenbias')

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
    # Call the OMDb API to fetch movie details
    api_url = f"http://www.omdbapi.com/?i={movie_id}&apikey={OMDB_API_KEY}"
    response = requests.get(api_url)
    
    if response.status_code != 200 or not response.json().get('Response') == 'True':
        abort(404, description="Movie not found or API error")
    
    movie = response.json()  # Parse the JSON response
    return render_template('movie_details.html', movie=movie)

if __name__ == '__main__':
    app.run()
