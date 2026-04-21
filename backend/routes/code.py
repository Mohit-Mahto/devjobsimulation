from flask import Blueprint, request, jsonify, current_app
import requests
import jwt
from functools import wraps

code_bp = Blueprint('code', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Missing token"}), 401
        try:
            token = auth_header.split(" ")[1]
            decoded = jwt.decode(token, current_app.config.get('JWT_SECRET'), algorithms=['HS256'])
            request.user = decoded
        except Exception as e:
            return jsonify({"error": "Invalid or expired token"}), 401
        return f(*args, **kwargs)
    return decorated

@code_bp.route('/run-code', methods=['POST'])
@token_required
def run_code():
    data = request.get_json()
    source_code = data.get('source_code')
    language_id = data.get('language_id', 71) # 71 is Python in Judge0

    if not source_code:
        return jsonify({"error": "Source code is required"}), 400

    # For free users, check limits in a real scenario.
    # Here we simulate access control based on user plan
    user_plan = request.user.get('plan', 'free')
    
    # In a full app, we would query the DB for submission count today.
    # We will assume they have limits if free.
    
    url = f"{current_app.config['JUDGE0_URL']}/submissions?base64_encoded=false&wait=true"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # If using RapidAPI
    api_key = current_app.config.get('JUDGE0_API_KEY')
    if api_key:
        headers["X-RapidAPI-Key"] = api_key
        headers["X-RapidAPI-Host"] = "judge0-ce.p.rapidapi.com"

    payload = {
        "source_code": source_code,
        "language_id": language_id
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        
        # Map output
        output = result.get('stdout') or result.get('stderr') or result.get('compile_output')
        
        # Award XP if it ran successfully (status id 3 is accepted)
        if result.get('status', {}).get('id') == 3:
            db = current_app.db
            db.users.update_one({"email": request.user['email']}, {"$inc": {"xp": 10}})
            
        return jsonify({
            "output": output,
            "status": result.get('status', {}).get('description'),
            "error": result.get('error')
        }), 200
        
    except Exception as e:
        # Fallback if Judge0 is not configured or offline
        if not api_key:
             return jsonify({
                 "output": "Simulated output: " + source_code,
                 "status": "Accepted (Simulated)",
                 "error": None,
                 "warning": "Judge0 API Key missing. Returning simulated output."
             }), 200
             
        return jsonify({"error": str(e)}), 500

@code_bp.route('/predict-role', methods=['POST'])
@token_required
def predict_role():
    data = request.get_json()
    code = data.get('code', '').lower()

    if not code:
        return jsonify({"error": "No code provided"}), 400

    # Rule-based logic
    if 'for' in code or 'while' in code or 'def ' in code or 'class ' in code:
        role = "Backend Developer"
    elif 'import pandas' in code or 'import numpy' in code or '[' in code:
        role = "Data Analyst"
    else:
        role = "Frontend Developer"
        
    # Update role in DB
    db = current_app.db
    db.users.update_one({"email": request.user['email']}, {"$set": {"role": role}})

    return jsonify({
        "role": role,
        "message": f"Based on your code, you look like a {role}!"
    }), 200
