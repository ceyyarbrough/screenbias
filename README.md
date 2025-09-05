
# ScreenBias: Flask Movie Review & Search Platform

ScreenBias is a modular Flask web application for searching, reviewing, and exploring movies and TV shows, with a focus on political/cultural categorization and data-driven visualizations. It features user authentication, registration, OMDb API integration, interactive review reactions, profanity/URL filtering, and a modern, responsive UI. The codebase is thoroughly commented and ready for future PostgreSQL integration.


## Purpose

ScreenBias allows users to:
- Search for movies and TV shows using the OMDb API
- Browse categorized galleries (by year, actor, director, political leaning, and most/recently reviewed)
- Register and log in to review movies (reviews require login)
- React to reviews with thumbs up/down (login required, AJAX updates)
- Explore stats and legacy pages
- View interactive visualizations of ratings by genre, year, and country
- Enjoy a themed, mobile-friendly, and secure experience


## Folder Structure

```
.
├── app.py                        # Entry point to run the Flask app
├── requirements.txt              # Python dependencies
├── templates/                    # Jinja2 HTML templates
│   ├── base.html                 # Main layout, navbar, and theming
│   ├── index.html                # Home page with galleries
│   ├── login.html                # Login form
│   ├── register.html             # Registration form
│   ├── movie_details.html        # Movie details page (reviews, reactions)
│   ├── search_results.html       # Search results page
│   ├── right.html, left.html, center.html # Legacy pages
│   ├── stats.html                # Stats page (tables, Chart.js visualizations)
│   ├── actors_*.html, directors_*.html, movies_*.html, tv_*.html # Category pages (by leaning)
│   └── ...                       # Other supporting templates (profile, etc.)
├── screenbias/                   # Main application package
│   ├── __init__.py               # App factory, context processor, module imports
│   ├── routes.py                 # Main navigation, galleries, stats, profile, and static page routes
│   ├── auth.py                   # Login/logout/authentication logic
│   ├── register.py               # Registration logic (future DB ready)
│   ├── omdb.py                   # OMDb API integration for home/galleries
│   ├── legacy.py                 # Legacy routes for old pages
│   ├── search.py                 # Search route using OMDb API
│   ├── details.py                # Movie details route (login required, review/reactions)
│   ├── models.py                 # SQLAlchemy models for reviews and reactions
│   ├── delete_review.py          # Route for deleting reviews
│   └── ...                       # Additional modules as needed
└── README.md                     # Project documentation
```


## File/Module Details

- **app.py**: Starts the Flask app. Use `python app.py` to launch.
- **screenbias/__init__.py**: Initializes the Flask app, sets up the template/static folders, context processor for year, and imports all route modules.
- **screenbias/routes.py**: Main navigation, galleries (by leaning, most/recently reviewed), stats, and profile page routes.
- **screenbias/auth.py**: Handles login/logout and session management.
- **screenbias/register.py**: Handles user registration (email, phone, name, country). Ready for future PostgreSQL integration.
- **screenbias/omdb.py**: Home page and galleries, pulls data from OMDb API (by year, actor, director, most/recently reviewed).
- **screenbias/legacy.py**: Legacy routes for old right/left/center pages.
- **screenbias/search.py**: Search route, queries OMDb API and displays results.
- **screenbias/details.py**: Movie details page, requires login to review, supports thumbs up/down reactions (AJAX), and profanity/URL filtering.
- **screenbias/models.py**: SQLAlchemy models for reviews and review reactions.
- **screenbias/delete_review.py**: Route for deleting reviews from the profile page.
- **templates/**: All HTML templates, using Bootstrap 5 and custom CSS for theming and responsiveness.


## Features

- User registration (email, phone, name, country, country dropdown)
- User login/logout (session management)
- Responsive navigation bar with dropdowns and search
- Home page galleries: newest (2025 only), by actor, by director, most reviewed, recently reviewed
- OMDb API integration for all movie/TV data
- Profile page for editing/deleting reviews
- Thumbs up/down reactions for reviews (login required, AJAX, live update)
- Profanity and URL filtering for all reviews (backend and frontend)
- Stats page with tables and Chart.js visualizations (by genre, year, country)
- Color-coded badges for review leaning (left/center/right)
- Secure session management
- Modern, mobile-friendly UI (Bootstrap 5, custom CSS)
- Legal disclaimer in the footer
- All code and templates are thoroughly commented for maintainability
- Modular Python codebase, ready for PostgreSQL integration


## Usage

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2. **Run the app:**
    ```bash
    python app.py
    ```
3. **Access the app:** Open your browser to `http://127.0.0.1:5000`
4. **Register/Login:** Use the green buttons in the navbar to register or log in.
5. **Search/Browse:** Use the search bar or navigation dropdowns to explore movies and TV shows.
6. **Review/React:** Submit reviews and react with thumbs up/down (login required).
7. **Profile:** Edit or delete your reviews from the profile page.
8. **Stats:** View interactive stats and visualizations on the stats page.


## Environment Variables
- Set your OMDb API key in the appropriate files or as an environment variable for production.


## PostgreSQL Integration (Future)
- The registration logic is ready for SQLAlchemy/PostgreSQL integration. Uncomment and configure the code in `register.py` when ready.


## Purpose of the Site
ScreenBias is designed to help users explore, categorize, and review movies and TV shows with a focus on political/cultural context. It is secure, modern, and extensible for future features like user reviews, stats, and database-backed user management.


## Contributing
Contributions are welcome! Fork the repository and submit a pull request.


## License
MIT License
