import os
import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS
from database.db import db
from database.models import User, Attempt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from modules.claim import claim_bp
from modules.policy import policy_bp
from modules.triggers import trigger_bp
from modules.dashboard import dashboard_bp

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "super-secret-key-change-this"
jwt = JWTManager(app)

db_path = os.environ.get('DATABASE_URL')
if not db_path:
    if os.environ.get('VERCEL'):
        db_path = 'sqlite:////tmp/gigshield_v2.db'
    else:
        db_path = 'sqlite:///gigshield_v2.db'

app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(claim_bp)
app.register_blueprint(policy_bp)
app.register_blueprint(trigger_bp)
app.register_blueprint(dashboard_bp)

from database.models import User, Attempt
from flask import Flask, jsonify, render_template

@app.route("/")
def home():
    return render_template("user/login.html")

# --- USER FRONTEND ROUTES ---
@app.route("/login", methods=["GET"])
def ui_login():
    return render_template("user/login.html")

@app.route("/plans", methods=["GET"])
def ui_plans():
    return render_template("user/plans.html")

@app.route("/checkout", methods=["GET"])
def ui_checkout():
    return render_template("user/payment.html")

@app.route("/dashboard", methods=["GET"])
def ui_dashboard():
    return render_template("user/user_dashboard.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or "face_encoding" not in data:
        return jsonify({
            "message": "face_encoding is required"
        }), 400

    face_encoding = data["face_encoding"]

    # 🔍 Check duplicate
    existing_user = User.query.filter_by(face_encoding=face_encoding).first()

    if existing_user:

    # If already locked
        if existing_user.account_locked:
            
            attempt = Attempt(
            human_id=existing_user.human_id,
            face_encoding=face_encoding,
            attempt_type="LOCKED"
            )
            db.session.add(attempt)
            db.session.commit()

            return jsonify({
                "message": "Account is locked due to suspicious activity",
                "human_id": existing_user.human_id,
                "risk_score": existing_user.risk_score,
                "risk_level": existing_user.risk_level
            }), 403

    # Increase risk
        existing_user.risk_score += 10

        if existing_user.risk_score >= 30:
            existing_user.risk_level = "High"
            existing_user.account_locked = True
        elif existing_user.risk_score >= 10:
            existing_user.risk_level = "Medium"

        db.session.commit()
        
        attempt = Attempt(
        human_id=existing_user.human_id,
        face_encoding=face_encoding,
        attempt_type="DUPLICATE"
        )
        db.session.add(attempt)
        db.session.commit()

        return jsonify({
            "message": "User already exists",
            "human_id": existing_user.human_id,
            "risk_score": existing_user.risk_score,
            "risk_level": existing_user.risk_level,
            "account_locked": existing_user.account_locked
        }), 409

    # New user
    human_id = str(uuid.uuid4())

    new_user = User(
        human_id=human_id,
        face_encoding=face_encoding,
        risk_score=0,
        risk_level="Low"
    )

    db.session.add(new_user)
    db.session.commit()

    attempt = Attempt(
    human_id=human_id,
    face_encoding=face_encoding,
    attempt_type="NEW"
    )
    db.session.add(attempt)
    db.session.commit()
    
    return jsonify({
        "message": "User registered successfully",
        "human_id": human_id,
        "risk_score": 0,
        "risk_level": "Low"
    }), 201

@app.route("/admin/users", methods=["GET"])
@jwt_required()
def get_all_users():

    current_user = get_jwt_identity()

    users = User.query.all()

    result = []

    for user in users:
        result.append({
            "human_id": user.human_id,
            "face_encoding": user.face_encoding,
            "risk_score": user.risk_score,
            "risk_level": user.risk_level
        })

    return jsonify({
        "accessed_by": current_user,
        "total_users": len(result),
        "users": result
    }), 200

from datetime import datetime, timedelta

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "human_id" not in data or "face_encoding" not in data:
        return jsonify({"message": "human_id and face_encoding required"}), 400

    human_id = data["human_id"]
    face_encoding = data["face_encoding"]

    user = User.query.filter_by(human_id=human_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    now = datetime.utcnow()

    # 🔒 Permanent Lock Check
    if user.account_locked:
        return jsonify({
            "message": "Account permanently locked due to repeated violations"
        }), 403

    # ⏳ Temporary Lock Check
    if user.lock_until and user.lock_until > now:
        return jsonify({
            "message": "Account temporarily locked",
            "lock_until": user.lock_until,
            "lock_count": user.lock_count
        }), 403

    # 🔓 Auto unlock if time expired
    if user.lock_until and user.lock_until <= now:
        user.lock_until = None
        user.failed_attempts = 0
        db.session.commit()

    # ✅ Correct Login
    if user.face_encoding == face_encoding:

        user.failed_attempts = 0
        db.session.commit()

        attempt = Attempt(
            human_id=user.human_id,
            face_encoding=face_encoding,
            attempt_type="LOGIN_SUCCESS"
        )
        db.session.add(attempt)
        db.session.commit()
        
        access_token = create_access_token(identity=user.human_id)
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "human_id": user.human_id,
            "risk_level": user.risk_level,
            "risk_score": user.risk_score
        }), 200

    # ❌ Wrong Login
    user.failed_attempts += 1

    if user.failed_attempts >= 3:

        user.lock_count += 1
        user.failed_attempts = 0

        # 🔥 Exponential lock duration
        lock_days = 2 ** (user.lock_count - 1)
        user.lock_until = datetime.utcnow() + timedelta(days=lock_days)

        if user.lock_count >= 4:
            user.account_locked = True

        db.session.commit()

        attempt = Attempt(
            human_id=user.human_id,
            face_encoding=face_encoding,
            attempt_type="LOCKED"
        )
        db.session.add(attempt)
        db.session.commit()

        if user.account_locked:
            return jsonify({
                "message": "Account permanently locked due to repeated violations",
                "lock_count": user.lock_count
            }), 403

        return jsonify({
            "message": "Account temporarily locked",
            "lock_until": user.lock_until,
            "lock_count": user.lock_count
        }), 403


# ❌ Normal failed login (less than 3 attempts)
    db.session.commit()

    attempt = Attempt(
        human_id=user.human_id,
        face_encoding=face_encoding,
        attempt_type="LOGIN_FAILED"
    )
    db.session.add(attempt)
    db.session.commit()

    return jsonify({
        "message": "Invalid credentials",
        "failed_attempts": user.failed_attempts
    }), 401

@app.route("/admin", methods=["GET"])
def admin():
    return jsonify({"message": "Admin Endpoint Ready"})

@app.route("/admin/attempts", methods=["GET"])
def get_all_attempts():
    attempts = Attempt.query.all()

    result = []

    for attempt in attempts:
        result.append({
            "human_id": attempt.human_id,
            "face_encoding": attempt.face_encoding,
            "attempt_type": attempt.attempt_type,
            "created_at": attempt.created_at
        })

    return jsonify({
        "total_attempts": len(result),
        "attempts": result
    }), 200

@app.route("/admin/unlock/<human_id>", methods=["POST"])
def admin_unlock_user(human_id):

    user = User.query.filter_by(human_id=human_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    # 🔓 Reset all lock-related fields
    user.account_locked = False
    user.lock_until = None
    user.failed_attempts = 0
    user.lock_count = 0

    db.session.commit()

    # Log admin action
    attempt = Attempt(
        human_id=user.human_id,
        face_encoding=user.face_encoding,
        attempt_type="ADMIN_UNLOCK"
    )
    db.session.add(attempt)
    db.session.commit()

    return jsonify({
        "message": "User account unlocked successfully",
        "human_id": user.human_id
    }), 200

# ==============================
# DASHBOARD CLAIMS API (ADD THIS)
# ==============================

from database.models import Claim

@app.route("/admin/claims", methods=["GET"])
def get_claims():
    claims = Claim.query.all()

    result = []

    for c in claims:
        result.append({
            "claim_id": c.claim_id,
            "user_id": c.user_id,
            "amount": c.amount,
            "status": c.status,
            "timestamp": c.timestamp
        })

    return jsonify({
        "claims": result,
        "total_claims": len(result)
    })

@app.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()

    if data["username"] == "admin" and data["password"] == "1234":
        return jsonify({
            "message": "Login successful",
            "token": "admin-token"
        })
    else:
        return jsonify({"message": "Invalid credentials"}), 401
    
app.static_folder = 'static'

@app.route('/admin-dashboard')
def admin_dashboard():
    return render_template('index/index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        # Seed initial workers if empty
        if User.query.count() == 0:
            u1 = User(human_id="U01", face_encoding="mock_u01", current_city="Delhi NCR", lat=28.6139, lng=77.2090, is_active=True)
            u2 = User(human_id="U02", face_encoding="mock_u02", current_city="Tamil Nadu", lat=13.0827, lng=80.2707, is_active=True)
            u3 = User(human_id="U03", face_encoding="mock_u03", current_city="Delhi NCR", lat=28.7041, lng=77.1025, is_active=True)
            u4 = User(human_id="U04", face_encoding="mock_u04", current_city="Mumbai", lat=19.0760, lng=72.8777, is_active=False) 
            db.session.add_all([u1, u2, u3, u4])
            db.session.commit()
            
    app.run(debug=True)
    
def calculate_premium(risk_score):
    base_price = 50
    return base_price + (risk_score * 5)
