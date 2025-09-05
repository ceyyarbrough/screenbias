

# models.py
# Defines the SQLAlchemy models for storing movie reviews, ratings, and review reactions.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# This file is imported by the app factory (__init__.py)
db = SQLAlchemy()

# ReviewReaction model: stores thumbs up/down reactions for reviews
class ReviewReaction(db.Model):
    """
    Stores a user's thumbs up ('up') or thumbs down ('down') reaction for a review.
    Each user can react only once per review (enforced by unique constraint).
    """
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False, index=True)
    username = db.Column(db.String(64), nullable=False, index=True)
    reaction = db.Column(db.String(8), nullable=False)  # 'up' or 'down'
    __table_args__ = (db.UniqueConstraint('review_id', 'username', name='unique_review_user'),)

# Review model: stores movie reviews and ratings
class Review(db.Model):
    """
    Stores a user's review for a movie, including rating (0-100), review text, and creation time.
    """
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(32), nullable=False, index=True)
    username = db.Column(db.String(64), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 0 (left) to 100 (right)
    review_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Review {self.movie_id} {self.username} {self.rating}>'
