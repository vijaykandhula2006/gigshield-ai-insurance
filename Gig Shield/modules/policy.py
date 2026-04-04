from flask import Blueprint, request, jsonify

policy_bp = Blueprint('policy', __name__)

policies = []

@policy_bp.route('/policy/create', methods=['POST'])
def create_policy():
    data = request.json

    policy = {
        "user_id": data.get("user_id"),
        "premium": data.get("premium"),
        "status": "Active"
    }

    policies.append(policy)

    return jsonify({
        "message": "Policy created",
        "policy": policy
    })