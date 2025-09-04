# __init__.py
# Initializes the Flask app, sets up context processors, and imports all route modules.

import os
from flask import Flask

# Explicitly set the template folder to the project-level templates directory
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'))
# Secret key for session management (should be changed in production)
app.secret_key = 'API Key Goes Here'


# Context processor to inject the current year into all templates
# This allows you to use {{ year }} in any template

def inject_year():
    from datetime import datetime
    return {'year': datetime.now().year}
app.context_processor(inject_year)

# Import route modules after app/context processor to avoid circular import issues
from . import routes, auth, omdb, legacy, search, details, register
