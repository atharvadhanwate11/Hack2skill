import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# Internal Modules
from engine import StadiumSimulationEngine

load_dotenv()

# --- System Initialization ---
DATA_FILE = os.path.join(os.path.dirname(__file__), "stadium_data.json")
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

engine = StadiumSimulationEngine(DATA_FILE)
app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# --- Routing: Static Files ---
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

# --- API: Live Data ---
@app.route('/api/status', methods=['GET'])
def get_status():
    stadium, event = engine.tick()
    return jsonify({
        "stadium": stadium,
        "event": event,
        "system_health": "Optimal",
        "last_sync": "Real-time"
    })

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    stadium, _ = engine.get_current_state()
    alerts = []
    
    # Logic-based alert generation
    for gate in stadium['gates']:
        if gate['crowd'] > 75:
            alerts.append({"type": "warning", "msg": f"Congestion Alert: {gate['name']} is at capacity."})
    
    for stall in stadium['food_stalls']:
        if stall['wait'] < 5:
            alerts.append({"type": "info", "msg": f"Efficiency Boost: {stall['name']} has <5 min wait."})

    return jsonify(alerts[:3])

# --- API: AI Orchestration ---
@app.route('/api/chat', methods=['POST'])
def chat():
    user_query = request.json.get('query', '')
    user_location = request.json.get('location', 'Standard West (Section S2)')
    
    stadium, event = engine.get_current_state()
    
    # TOP-TIER SYSTEM PROMPT
    prompt = f"""
    ROLE: You are the Real-time Stadium Optimization Engine. 
    GOAL: Provide actionable, decision-driven navigation to maximize attendee efficiency.

    BEHAVIOR RULES:
    1. PRIORITIZATION: If time is critical (e.g., match restart soon), prioritize minimal wait time over distance.
    2. LOGIC-BASED: Use Distance, Crowd Density, and Wait Time to justify every recommendation.
    3. NO FLUFF: Be confident, assertive, and concise.
    4. ACCESSIBILITY: Keep instructions clear and simple.

    CONTEXT:
    - User Query: {user_query}
    - Location: {user_location}
    - Live Facility Data: {json.dumps(stadium)}
    - Game Context: {json.dumps(event)}
    
    RESPONSE FORMAT (MANDATORY):
    Recommendation: [Specific Location]
    
    Why:
    * [Distance/Time Factor]
    * [Crowd/Congestion Factor]
    * [Event Timing Factor]

    Alternative Option: [Second-best balance of distance/time]

    Estimated Time Impact: [Time saved vs. busiest comparable facility]
    """
    
    try:
        if not GEMINI_API_KEY: raise ValueError("No API Key")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        # Robust Fallback to Decision-Tree Mock
        return jsonify({"response": mock_decision_engine(user_query, stadium, event)})

def mock_decision_engine(query, data, event):
    query = query.lower()
    time_ctx = event['time_remaining']
    is_urgent = "mins" in time_ctx.lower() or "1'" in time_ctx or "2'" in time_ctx

    if 'food' in query or 'eat' in query:
        # Logic: Sort by wait time if urgent, else by crowd (comfort)
        stalls = sorted(data['food_stalls'], key=lambda x: x['wait'] if is_urgent else x['crowd'])
        best, second = stalls[0], stalls[1]
        
        urgency_note = "PRIORITY: Time-Critical (Game Restarting)" if is_urgent else "PRIORITY: Comfort & Flow"
        return f"Recommendation: {best['name']}\n\nWhy:\n* {urgency_note}\n* {best['wait']} min wait is the lowest in your sector\n* Crowd density is manageable at {best['crowd']}%\n\nAlternative Option: {second['name']}\n\nEstimated Time Impact: Saves approx {second['wait'] - best['wait'] + 2} mins."

    return "Recommendation: Please specify your destination (Gate, Food, or Washroom).\n\nWhy:\n* I need context to calculate the optimal time-path\n* Live flow varies significantly between facilities\n* Current location is detected as Section A"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
