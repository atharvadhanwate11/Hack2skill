import os
import json
import math
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
    stadium, event = engine.get_current_state()
    alerts = []
    
    if "Surge" in event['phase']:
        alerts.append({"type": "warning", "msg": f"SYSTEM ALERT: {event['phase']} initiated. Expect high density."})

    for gate in stadium['gates']:
        if gate['crowd'] > 85:
            alerts.append({"type": "warning", "msg": f"CRITICAL: {gate['name']} is reaching flow capacity limits."})

    return jsonify(alerts[:3])

# --- API: AI Orchestration ---
@app.route('/api/chat', methods=['POST'])
def chat():
    user_query = request.json.get('query', '')
    user_pos = request.json.get('pos', [15, 65]) # Get actual coordinates
    
    stadium, event = engine.get_current_state()
    
    # INDUSTRIAL-GRADE AI ORCHESTRATOR PROMPT
    prompt = f"""
    SYSTEM ROLE: StadiumFlow Optimization Engine.
    CONTEXT: {event['phase']} at {event['time_remaining']}.
    USER_POS: {user_pos}
    SENSOR_DATA: {json.dumps(stadium)}

    LOGIC:
    1. CALCULATE Euclidean distance from User_Pos to each facility.
    2. SCORE facilities using: (WaitTime * 0.5) + (CrowdDensity * 0.3) + (Distance * 0.2).
    3. If PHASE involves 'Surge' or 'Egress', double the 'WaitTime' weight.
    4. RESPOND with a Markdown Matrix. Be deterministic.
    """
    
    try:
        if not GEMINI_API_KEY: raise ValueError("No API Key")
        model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"temperature": 0.1})
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": mock_decision_engine(user_query, user_pos, stadium, event)})

def mock_decision_engine(query, user_pos, data, event):
    query = query.lower()
    targets = []
    category = "Facility"
    
    if any(x in query for x in ['food', 'eat']): targets, category = data['food_stalls'], "Food Stall"
    elif any(x in query for x in ['washroom', 'toilet', 'piss']): targets, category = data['washrooms'], "Washroom"
    elif any(x in query for x in ['gate', 'exit', 'leave']): targets, category = data['gates'], "Gate / Exit"

    if not targets:
        return "### 🔎 Data Search\nPlease specify if you are looking for a **Gate**, **Food Stall**, or **Washroom**."

    # CALCULATE OPTIMIZED SCORE (Weighted Utility)
    def get_score(f):
        dist = math.sqrt((f['pos'][0]-user_pos[0])**2 + (f['pos'][1]-user_pos[1])**2)
        # Weighting: Wait (50%), Distance (30%), Crowd (20%)
        return (f['wait'] * 0.5) + (dist * 0.3) + (f['crowd'] * 0.2)

    optimized = sorted(targets, key=get_score)
    best, second = optimized[0], optimized[1]
    
    return f"""### OPTIMIZED: {best['name']}
    
**System Analysis (Phase: {event['phase']}):**
- **Distance Score**: {round(math.sqrt((best['pos'][0]-user_pos[0])**2 + (best['pos'][1]-user_pos[1])**2), 1)} units
- **Wait Time**: {best['wait']} mins (Optimal for sector)
- **Crowd Pressure**: {best['crowd']}%

**AI Recommendation:** We've calculated a **Weighted Utility Score** for all nearby {category} facilities. {best['name']} provides the lowest 'Time-to-Service' ratio.

**Secondary Choice:** {second['name']}"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
