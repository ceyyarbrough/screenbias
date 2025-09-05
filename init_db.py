from screenbias import app
from screenbias.models import db

with app.app_context():
    db.create_all()
    print("Database tables created.")