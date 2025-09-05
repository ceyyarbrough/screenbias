
# __init__.py
# Initializes the Flask app, sets up context processors, configures the database, and imports all route modules.



import os
from flask import Flask
from flask_caching import Cache

# Explicitly set the template folder to the project-level templates directory

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
)

# Flask-Caching configuration (simple in-memory cache by default)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 3600  # 1 hour default
cache = Cache(app)

# Secret key for session management (should be set securely in production)
app.secret_key = os.environ.get('SCREENBIAS_SECRET_KEY', 'insecure-dev-key')
if app.secret_key == 'insecure-dev-key':
    import warnings
    warnings.warn('WARNING: Using insecure default secret key! Set SCREENBIAS_SECRET_KEY in your environment for production.')

# Database configuration (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///screenbias.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import and initialize SQLAlchemy
from .models import db
db.init_app(app)

# Context processor to inject the current year into all templates
# This allows you to use {{ year }} in any template
def inject_year():
    from datetime import datetime
    return {'year': datetime.now().year}
app.context_processor(inject_year)


# Import route modules after app/context processor to avoid circular import issues
# This ensures all routes are registered with the Flask app
from . import routes, auth, omdb, legacy, search, register, delete_review, details

# Debug: print all registered endpoints at startup
print("Registered endpoints:", [rule.endpoint for rule in app.url_map.iter_rules()])
