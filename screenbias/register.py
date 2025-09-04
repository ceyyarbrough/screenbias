"""
register.py
Handles user registration form and (future) database integration.
"""

from . import app
from flask import render_template, request, redirect, url_for, flash

# For future PostgreSQL integration
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy(app)
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     phone = db.Column(db.String(20), nullable=False)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     country = db.Column(db.String(2), nullable=False)

# Registration route: handles GET (show form) and POST (process registration)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        country = request.form.get('country')
        # Here you would add code to save to the database
        # Example (uncomment when db is set up):
        # user = User(email=email, phone=phone, first_name=first_name, last_name=last_name, country=country)
        # db.session.add(user)
        # db.session.commit()
        flash('Registration successful! (DB integration coming soon)', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')
