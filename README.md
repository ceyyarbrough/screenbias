# ScreenBias: Flask Movie Review & Search Platform

ScreenBias is a Flask-based web application for searching, reviewing, and exploring movies and TV shows, with a focus on political/cultural categorization. It features user authentication, registration, reCAPTCHA security, and a modern, responsive UI. The app is modularized for maintainability and ready for future PostgreSQL integration.

## Purpose

ScreenBias allows users to:
- Search for movies and TV shows using the OMDb API
- Browse categorized galleries (by year, actor, director, political leaning)
- Register and log in to review movies (reviews require login)
- Explore stats and legacy pages
- Enjoy a themed, mobile-friendly, and secure experience

## Folder Structure

```
.
├── run.py                        # Entry point to run the Flask app
├── requirements.txt              # Python dependencies
├── templates/                    # Jinja2 HTML templates
│   ├── base.html                 # Main layout, navbar, and theming
│   ├── index.html                # Home page with galleries
│   ├── login.html                # Login form with reCAPTCHA
│   ├── register.html             # Registration form with reCAPTCHA
│   ├── movie_details.html        # Movie details page
│   ├── search_results.html       # Search results page
│   ├── right.html, left.html, center.html # Legacy pages
│   ├── stats.html                # Stats page
│   ├── actors_*.html, directors_*.html, movies_*.html, tv_*.html # Category pages
│   └── ...                       # Other supporting templates
├── screenbias/                   # Main application package
│   ├── __init__.py               # App factory, context processor, module imports
│   ├── routes.py                 # Main navigation and static page routes
│   ├── auth.py                   # Login/logout/authentication logic
│   ├── register.py               # Registration logic (future DB ready)
│   ├── omdb.py                   # OMDb API integration for galleries/home
│   ├── legacy.py                 # Legacy routes for old pages
│   ├── search.py                 # Search route using OMDb API
│   ├── details.py                # Movie details route (login required)
│   └── ...                       # Additional modules as needed
└── README.md                     # Project documentation
```

## File/Module Details

- **run.py**: Starts the Flask app. Use `python run.py` to launch.
- **screenbias/__init__.py**: Initializes the Flask app, sets up the template folder, context processor for year, and imports all route modules.
- **screenbias/routes.py**: Main navigation and static page routes (movies, TV, actors, directors, stats).
- **screenbias/auth.py**: Handles login/logout, session management, and reCAPTCHA verification for login.
- **screenbias/register.py**: Handles user registration (email, phone, name, country, reCAPTCHA). Ready for future PostgreSQL integration.
- **screenbias/omdb.py**: Home page and galleries, pulls data from OMDb API (by year, actor, director).
- **screenbias/legacy.py**: Legacy routes for old right/left/center pages.
- **screenbias/search.py**: Search route, queries OMDb API and displays results.
- **screenbias/details.py**: Movie details page, requires login to review.
- **templates/**: All HTML templates, using Bootstrap 5 and custom CSS for theming and responsiveness.

## Features

- User registration (email, phone, name, country, country dropdown, reCAPTCHA)
- User login/logout (with reCAPTCHA)
- Responsive navigation bar with dropdowns and search
- Three home page galleries (newest, by actor, by director)
- OMDb API integration for all movie/TV data
- Stats and legacy pages
- Secure session management
- Modern, mobile-friendly UI (Bootstrap 5, custom CSS)
- All code and templates are thoroughly commented
- Modular Python codebase, ready for PostgreSQL integration

## Usage

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2. **Run the app:**
    ```bash
    python run.py
    ```
3. **Access the app:** Open your browser to `http://127.0.0.1:5000`
4. **Register/Login:** Use the green buttons in the navbar to register or log in. Registration and login both use Google reCAPTCHA for security.
5. **Search/Browse:** Use the search bar or navigation dropdowns to explore movies and TV shows.

## Environment Variables
- Set your OMDb API key and reCAPTCHA keys in the appropriate files or as environment variables for production.

## PostgreSQL Integration (Future)
- The registration logic is ready for SQLAlchemy/PostgreSQL integration. Uncomment and configure the code in `register.py` when ready.

## Purpose of the Site
ScreenBias is designed to help users explore, categorize, and review movies and TV shows with a focus on political/cultural context. It is secure, modern, and extensible for future features like user reviews, stats, and database-backed user management.

## Contributing
Contributions are welcome! Fork the repository and submit a pull request.

## License
MIT License
