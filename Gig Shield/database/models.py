from database.db import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    human_id = db.Column(db.String(100), unique=True, nullable=False)
    face_encoding = db.Column(db.Text, nullable=False)

    risk_score = db.Column(db.Integer, default=0)
    risk_level = db.Column(db.String(20), default="Low")

    # Geolocation / Active Verification
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    current_city = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)

    failed_attempts = db.Column(db.Integer, default=0)
    lock_until = db.Column(db.DateTime, nullable=True)
    lock_count = db.Column(db.Integer, default=0)
    account_locked = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime)
    
class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    human_id = db.Column(db.String(100), nullable=True)
    face_encoding = db.Column(db.Text, nullable=False)
    attempt_type = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Claim(db.Model):
    claim_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50))
    amount = db.Column(db.Integer)
    status = db.Column(db.String(50))
    timestamp = db.Column(db.String(50))
    plan = db.Column(db.String)
    verification_info = db.Column(db.String(200)) # e.g. "GPS Match: Delhi NCR"

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    count = db.Column(db.Integer)
    premium = db.Column(db.String(50))
    pct = db.Column(db.Integer)

class FraudAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    claim_id = db.Column(db.Integer, db.ForeignKey('claim.claim_id'))
    desc = db.Column(db.String(200))
    user_name = db.Column(db.String(100))
    risk_level = db.Column(db.String(50))
    resolved = db.Column(db.Boolean, default=False)

class EventLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    event_type = db.Column(db.String(50))
    time = db.Column(db.String(100))
    claims_generated = db.Column(db.Integer, default=0)