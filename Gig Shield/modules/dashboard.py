from flask import Blueprint, jsonify, request
from database.db import db
from database.models import User, Claim, Policy, FraudAlert, EventLog

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/admin/dashboard', methods=['GET'])
def get_dashboard():
    # Stats
    total_users = User.query.count()
    active_policies = db.session.query(db.func.sum(Policy.count)).scalar() or 0
    claims_triggered = Claim.query.count()
    fraud_alerts_count = FraudAlert.query.filter_by(resolved=False).count()

    # Lists
    recent_claims = []
    for c in Claim.query.order_by(Claim.claim_id.desc()).limit(5).all():
        recent_claims.append({
            "id": f"#CLM-{c.claim_id}",
            "user": c.user_id,
            "amount": f"₹{c.amount}",
            "status": c.status.lower(),
            "date": c.timestamp,
            "verification": c.verification_info
        })

    fraud_alerts = []
    for f in FraudAlert.query.filter_by(resolved=False).all():
        fraud_alerts.append({
            "id": f"#CLM-{f.claim_id}",
            "desc": f.desc,
            "user": f.user_name,
            "risk": f.risk_level
        })

    trigger_log = []
    for t in EventLog.query.order_by(EventLog.id.desc()).limit(5).all():
        trigger_log.append({
            "name": t.name,
            "type": t.event_type,
            "time": t.time,
            "claims": t.claims_generated
        })

    policies = []
    for p in Policy.query.all():
        policies.append({
            "type": p.type,
            "count": p.count,
            "premium": p.premium,
            "pct": p.pct
        })

    return jsonify({
        "stats": {
            "users": total_users,
            "policies": active_policies,
            "claims": claims_triggered,
            "fraud": fraud_alerts_count
        },
        "recent_claims": recent_claims,
        "fraud_alerts": fraud_alerts,
        "trigger_log": trigger_log,
        "policies": policies
    })

@dashboard_bp.route('/admin/resolve_fraud', methods=['POST'])
def resolve_fraud():
    data = request.json
    claim_id_str = data.get("claim_id", "")  # e.g. "#CLM-2843"
    action = data.get("action")  # "ok" or "deny"

    if claim_id_str.startswith("#CLM-"):
        claim_id = int(claim_id_str.split("-")[1])
    else:
        claim_id = int(claim_id_str)

    alert = FraudAlert.query.filter_by(claim_id=claim_id).first()
    if alert:
        alert.resolved = True
        claim = Claim.query.filter_by(claim_id=claim_id).first()
        if claim:
            if action == 'ok':
                 claim.status = 'Approved'
            elif action == 'deny':
                 claim.status = 'Rejected'
        db.session.commit()
        return jsonify({"message": f"Fraud alert resolved and claim updated."})
    
    return jsonify({"message": "Fraud alert not found"}), 404

@dashboard_bp.route('/admin/approve_all_pending', methods=['POST'])
def approve_all_pending():
    pending_claims = Claim.query.filter(Claim.status.ilike('pending')).all()
    count = 0
    for claim in pending_claims:
        claim.status = 'Approved'
        count += 1
    db.session.commit()
    return jsonify({"message": f"{count} pending claims approved."})

@dashboard_bp.route('/user/<user_id>/dashboard', methods=['GET'])
def user_dashboard(user_id):
    # Fetch user claims
    user_claims = Claim.query.filter_by(user_id=user_id).order_by(Claim.claim_id.desc()).all()
    
    total_claims = len(user_claims)
    total_payout = sum([c.amount for c in user_claims if c.status.lower() == 'approved' or c.status.lower() == 'auto-approved'])
    
    # Try to infer plan from claims, otherwise fallback to "Standard Shield"
    active_plan = user_claims[0].plan if user_claims and user_claims[0].plan else "Standard Shield"
    
    recent_claims = []
    for c in user_claims[:5]:
        recent_claims.append({
            "id": f"#CLM-{c.claim_id}",
            "amount": f"₹{c.amount}",
            "status": c.status.lower(),
            "date": c.timestamp,
            "plan": c.plan,
            "verification": c.verification_info
        })
        
    return jsonify({
        "user_id": user_id,
        "active_plan": active_plan,
        "stats": {
            "total_claims": total_claims,
            "total_payout": total_payout
        },
        "recent_claims": recent_claims
    })
