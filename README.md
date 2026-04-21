# Devjob Simulator App

A complete, production-ready SaaS web application featuring real authentication, database storage, and a code execution engine.

## Features
- JWT-based authentication (Register / Login)
- MongoDB integration to store users and progress
- Code Execution using Judge0 API
- Role Prediction based on code analysis
- XP System and Tasks
- Mock Upgrade/Payment System

## Directory Structure
- `/backend`: Python Flask API
- `/frontend`: HTML, CSS, JavaScript (Vanilla)

## Local Development Setup

### 1. Backend Setup
1. Open a terminal and navigate to the backend folder:
   ```bash
   cd devjob-simulator/backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set environment variables. Create a `.env` file in the `backend/` directory:
   ```env
   MONGO_URI=mongodb://localhost:27017/devjob
   JWT_SECRET=your_super_secret_key
   JUDGE0_API_KEY=your_rapidapi_judge0_key
   ```
5. Run the server:
   ```bash
   python app.py
   ```
   *The server will start on `http://localhost:5000`.*

### 2. Frontend Setup
1. Ensure the backend is running.
2. In the `frontend/js/app.js` and `frontend/js/auth.js`, the `API_URL` is set to `http://localhost:5000/api`.
3. Open `frontend/login.html` directly in your browser or use a local server like Live Server (VSCode).

## Deployment to Render

1. Push this repository to GitHub.
2. Go to [Render](https://render.com/).
3. Create a **Blueprint Instance** and connect your repository.
4. Render will automatically detect the `render.yaml` file and create:
   - A Web Service for the Flask Backend.
   - A Static Site for the Frontend.
5. **Important**: Go to the Render Dashboard for your Backend service and set the Environment Variables (`MONGO_URI`, `JWT_SECRET`, `JUDGE0_API_KEY`).
6. **Frontend Configuration**: Once the backend is deployed, copy its URL. Update `API_URL` in `frontend/js/app.js` and `auth.js` to point to the new deployed backend URL before deploying the frontend, or deploy again.

## License
MIT
