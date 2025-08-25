# Flask Movie Search App

This is a Flask-based web application that allows users to search for movies using the OMDb API and view detailed information about selected movies.

## Features

- **Search Movies**: Users can search for movies by title.
- **View Movie Details**: Clicking on a movie displays detailed information such as the title, year, genre, director, actors, and plot.
- **Categorized Pages**: Includes predefined pages for "Right Wing", "Left Wing", and "Center Wing" content.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.7 or higher
- `pip` (Python package manager)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```
2. Create a Virtual Environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set Up the OMDB API Key:
    - Sign up for an API key at OMDb API.
    - Open `app.py` and set the `OMDB_API_KEY` variable with your API key:
        ```bash
        OMDB_API_KEY = 'your_api_key_here'
        ```

## Usage

1. Run the Application:
    ```bash
    flask run
    ```
2. Access the Application: Open your browser and navigate to `http://127.0.0.1:5000`.
3. Search for Movies:
    - Use the search bar to find movies by title.
    - Click on a movie to view detailed information.

## File Structure

```text
.
├── app.py                 # Main application file
├── templates/             # HTML templates
│   ├── index.html         # Home page
│   ├── search_results.html # Search results page
│   ├── movie_details.html # Movie details page
│   ├── right.html         # Right Wing page
│   ├── left.html          # Left Wing page
│   └── center.html        # Center Wing page
├── static/                # Static files (CSS, JS, images)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## API Reference

This app uses the `OMDB API` to fetch movie data. Below are the key endpoints:

- **Search Movies**: `https://www.omdbapi.com/?apikey=YOUR_API_KEY&s=QUERY`
- **Get Movie Details**: `https://www.omdbapi.com/?apikey=YOUR_API_KEY&i=MOVIE_ID`

## Error Handling

- If no search query is provided, the app displays an error message on the search results page.
- If the OMDb API returns an error or no results, the app gracefully handles the error and informs the user.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - Python web framework
- [OMDb API](http://www.omdbapi.com/) - Movie database API
