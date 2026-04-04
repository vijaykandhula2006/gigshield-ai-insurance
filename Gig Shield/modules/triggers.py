from flask import Blueprint, request, jsonify
from datetime import datetime
import random
from database.db import db
from database.models import Claim, EventLog

trigger_bp = Blueprint('trigger', __name__)

@trigger_bp.route('/trigger-event', methods=['POST'])
def trigger_event():
    data = request.json
    event_type = data.get("event_type", "rain")
    location = data.get("location", "Unknown Location")
    
    # Find all eligible users in this location
    from database.models import User
    eligible_workers = User.query.filter_by(current_city=location, is_active=True).all()
    claims_generated = len(eligible_workers)
    
    # Create EventLog
    event_log = EventLog(
        name=f"{event_type.capitalize()} Event - {location}",
        event_type=event_type,
        time=datetime.now().strftime("%Y-%m-%d %H:%M"),
        claims_generated=claims_generated
    )
    db.session.add(event_log)
    
    # Create Claims for eligible workers only
    for worker in eligible_workers:
        claim = Claim(
            user_id=worker.human_id,
            amount=random.randint(450, 600), # Realistic parametric amount
            status="Auto-Approved",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
            plan="Standard Shield",
            verification_info=f"GPS Match: {location} Zone"
        )
        db.session.add(claim)

    db.session.commit()

    return jsonify({
        "message": "Trigger executed",
        "count": claims_generated,
        "event_type": event_type,
        "location": location
    })