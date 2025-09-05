
# auth.py
# Handles user authentication: login, logout, and session management.

from . import app
from flask import render_template, request, redirect, url_for, session, flash
import requests


# Simple user store for demonstration (replace with a database in production)
import os
import warnings
USERS = {
    os.environ.get('SCREENBIAS_USER1', 'chris'): os.environ.get('SCREENBIAS_PASS1', 'password1'),
    os.environ.get('SCREENBIAS_USER2', 'nicole'): os.environ.get('SCREENBIAS_PASS2', 'password2'),
}
if USERS.get('chris') == 'password1' or USERS.get('nicole') == 'password2':
    warnings.warn('WARNING: Using demo user credentials! Set SCREENBIAS_USER1/2 and SCREENBIAS_PASS1/2 in your environment for production.')

# Logout route: logs out the current user and redirects to login page
@app.route('/logout')
def logout():
    """
    Logs out the current user by removing 'username' from session.
    """
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# Login route: handles GET (show form) and POST (authenticate)
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page. On POST, authenticates user against USERS dict and sets session.
    On GET, displays the login form.
    """
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
