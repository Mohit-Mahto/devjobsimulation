from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for frontend
    CORS(app)

    # Connect to MongoDB directly
    try:
        app.mongo_client = MongoClient(app.config["MONGO_URI"])
        # Use 'devjob' database to prevent conflicting with other apps on the same cluster
        app.db = app.mongo_client["devjob"]
        # Test connection
        app.mongo_client.admin.command('ping')
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

    # Register blueprints
    from routes.auth import auth_bp
    from routes.code import code_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(code_bp, url_prefix='/api/code')

    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"}), 200

    # Ensure indexes
    if hasattr(app, 'db'):
        app.db.users.create_index("email", unique=True)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
