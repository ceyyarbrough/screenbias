
# legacy.py
# Contains legacy routes for old pages (rightwing, leftwing, centerwing).
# These are static pages for backward compatibility.

from . import app
from flask import render_template


# Legacy right wing films page
@app.route('/rightwing')
def rightwing():
    """
    Legacy static page for right wing films (for backward compatibility).
    """
    return render_template('right.html', name='rightscreenbias')


# Legacy left wing films page
@app.route('/leftwing')
def leftwing():
    """
    Legacy static page for left wing films (for backward compatibility).
    """
    return render_template('left.html', name='leftscreenbias')


# Legacy centrist films page
@app.route('/centerwing')
def centerwing():
    """
    Legacy static page for centrist films (for backward compatibility).
    """
    return render_template('center.html', name='centerscreenbias')
