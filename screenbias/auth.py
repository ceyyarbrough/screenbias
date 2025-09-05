
# auth.py
# Handles user authentication: login, logout, and session management.

from . import app
from flask import render_template, request, redirect, url_for, session, flash
import requests

# Simple user store for demonstration (replace with a database in production)
USERS = {
    'chris': 'password1',
    'nicole': 'password2',
}

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# Login route: handles GET (show form) and POST (authenticate)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')
