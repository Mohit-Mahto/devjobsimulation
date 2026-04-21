from flask import Blueprint, request, jsonify, current_app
import bcrypt
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

def generate_token(user_id, email, role, plan):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': str(user_id),
        'email': email,
        'role': role,
        'plan': plan
    }
    return jwt.encode(payload, current_app.config.get('JWT_SECRET'), algorithm='HS256')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    db = current_app.db
    if db.users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    # Hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    user = {
        "email": email,
        "password_hash": hashed.decode('utf-8'),
        "role": "Beginner",
        "xp": 0,
        "plan": "free",
        "completed_tasks": []
    }

    result = db.users.insert_one(user)
    
    token = generate_token(result.inserted_id, email, user["role"], user["plan"])
    
    return jsonify({
        "message": "User registered successfully", 
        "token": token,
        "user": {
            "email": email,
            "role": user["role"],
            "xp": user["xp"],
            "plan": user["plan"]
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    db = current_app.db
    user = db.users.find_one({"email": email})

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_token(user['_id'], user['email'], user['role'], user['plan'])

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "email": user['email'],
            "role": user['role'],
            "xp": user['xp'],
            "plan": user['plan']
        }
    }), 200

@auth_bp.route('/upgrade-plan', methods=['POST'])
def upgrade_plan():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Missing token"}), 401

    try:
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(token, current_app.config.get('JWT_SECRET'), algorithms=['HS256'])
        user_email = decoded['email']
        
        db = current_app.db
        db.users.update_one({"email": user_email}, {"$set": {"plan": "pro"}})
        
        user = db.users.find_one({"email": user_email})
        new_token = generate_token(user['_id'], user['email'], user['role'], user['plan'])

        return jsonify({
            "message": "Plan upgraded to Pro successfully",
            "token": new_token,
            "plan": "pro"
        }), 200
    except Exception as e:
        return jsonify({"error": "Invalid or expired token"}), 401
