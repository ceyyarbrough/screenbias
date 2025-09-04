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

# Login route: handles GET (show form) and POST (authenticate)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # --- reCAPTCHA v2 verification ---
        recaptcha_response = request.form.get('g-recaptcha-response')
        recaptcha_secret = 'Secret Key Goes Here'  # Replace with your reCAPTCHA v2 secret key
        recaptcha_verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        recaptcha_payload = {
            'secret': recaptcha_secret,
            'response': recaptcha_response,
            'remoteip': request.remote_addr
        }
        recaptcha_result = requests.post(recaptcha_verify_url, data=recaptcha_payload).json()
        if not recaptcha_result.get('success'):
            flash('CAPTCHA verification failed. Please try again.', 'danger')
            return render_template('login.html')
        # --- End reCAPTCHA v2 verification ---
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# Logout route: removes user from session
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))
