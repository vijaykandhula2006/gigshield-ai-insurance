from flask import Blueprint, jsonify, request
from database.db import db
from database.models import Claim
from datetime import datetime

claim_bp = Blueprint('claim', __name__)

@claim_bp.route('/claims/<user_id>', methods=['GET'])
def get_claims(user_id):
    user_claims = Claim.query.filter_by(user_id=user_id).all()
    result = []
    for c in user_claims:
        result.append({
            "claim_id": c.claim_id,
            "amount": c.amount,
            "status": c.status,
            "timestamp": c.timestamp
        })
    return jsonify(result)

@claim_bp.route('/admin/claims', methods=['POST'])
def create_admin_claim():
    data = request.json
    new_claim = Claim(
        user_id=data.get('user_id', 'U01'),
        amount=data.get('amount', 500),
        status='Pending',
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
        plan=data.get('plan', 'Standard Shield')
    )
    db.session.add(new_claim)
    db.session.commit()
    return jsonify({"message": "Claim filed by admin", "claim_id": new_claim.claim_id})

@claim_bp.route('/admin/claims/resolve', methods=['POST'])
def resolve_claim():
    data = request.json
    claim_id_str = str(data.get('claim_id'))
    action = data.get('action') # 'approved' or 'rejected'

    if claim_id_str.startswith("#CLM-"):
        cid = int(claim_id_str.split("-")[1])
    else:
        cid = int(claim_id_str)

    claim = Claim.query.get(cid)
    if not claim:
        return jsonify({"message": "Claim not found"}), 404

    claim.status = action.capitalize()
    db.session.commit()
    return jsonify({"message": f"Claim {action} successfully"})