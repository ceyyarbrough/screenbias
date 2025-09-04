# legacy.py
# Contains legacy routes for old pages (rightwing, leftwing, centerwing).

from . import app
from flask import render_template

# Legacy right wing films page
@app.route('/rightwing')
def rightwing():
    return render_template('right.html', name='rightscreenbias')

# Legacy left wing films page
@app.route('/leftwing')
def leftwing():
    return render_template('left.html', name='leftscreenbias')

# Legacy centrist films page
@app.route('/centerwing')
def centerwing():
    return render_template('center.html', name='centerscreenbias')
