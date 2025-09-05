
# delete_review.py
# Adds a route to allow users to delete their own reviews from the profile page.

from . import app
from flask import session, redirect, url_for, flash
from .models import db, Review

# Route to delete a review by its ID (POST only, user must own the review)
@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    """
    Allows a logged-in user to delete their own review by review_id.
    Redirects to login if not logged in, or to profile if not owner.
    """
    if 'username' not in session:
        flash('You must be logged in to delete reviews.', 'warning')
        return redirect(url_for('login'))
    review = Review.query.get_or_404(review_id)
    if review.username != session['username']:
        flash('You can only delete your own reviews.', 'danger')
        return redirect(url_for('profile'))
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted.', 'success')
    return redirect(url_for('profile'))
