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
    
    # INDUSTRIAL-GRADE AI ORCHESTRATOR PROMPT
    prompt = f"""
    SYSTEM ROLE: You are the StadiumFlow Real-time Navigation Logic Engine. 
    DATA CONTEXT:
    - User Current Pos: {user_location}
    - Stadium Sensors: {json.dumps(stadium)}
    - Game Context: {json.dumps(event)}

    ALGORITHM RULES:
    1. SPATIAL MATH: Calculate 'Proximity' using visual [x,y] coordinates from the sensors.
    2. URGENCY WEIGHTING: 
       - If Game Time < 5 mins or 'Restarts' soon: Weight logic toward MINIMUM WAIT TIME.
       - Otherwise: Weight logic toward MINIMUM CROWD DENSITY.
    3. VALIDATION: Only recommend facilities that exist in the provided 'Stadium Sensors' list.
    4. FORMAT: Use the following structural template strictly. No conversational filler.

    ### RECOMMENDATION: [PLACE NAME]
    
    **Reasoning Matrix:**
    | Factor | Status | Impact Score |
    | :--- | :--- | :--- |
    | **Spatial Distance** | [Calculated distance] | [High/Mid/Low] |
    | **Wait Efficiency** | [Wait Time] min queue | [High/Mid/Low] |
    | **Crowd Comfort** | [Crowd %] density | [Optimized/Congested] |

    **AI Insight:** [One technical sentence on why this choice is optimal for the current game clock: {event['time_remaining']}].

    **Alternative:** [Next best facility]
    """
    
    try:
        if not GEMINI_API_KEY: raise ValueError("No API Key")
        # Initialize with low temperature for deterministic reliability
        model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"temperature": 0.1})
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        # Robust Fallback to Decision-Tree Mock
        return jsonify({"response": mock_decision_engine(user_query, stadium, event)})

def mock_decision_engine(query, data, event):
    query = query.lower()
    time_ctx = event.get('time_remaining', '10 mins')
    is_urgent = any(x in time_ctx.lower() for x in ["mins", "1'", "2'", "3'"])

    # Mapping keywords to data categories
    target_data = []
    category = "Facility"
    
    if any(x in query for x in ['food', 'eat', 'hungry', 'snack']):
        target_data = data['food_stalls']
        category = "Food Stall"
    elif any(x in query for x in ['washroom', 'toilet', 'piss', 'restroom', 'bathroom']):
        target_data = data['washrooms']
        category = "Washroom"
    elif any(x in query for x in ['gate', 'exit', 'leave', 'out']):
        target_data = data['gates']
        category = "Gate / Exit"

    if target_data:
        # Optimization Logic: Sort by wait time during urgency, else by crowd density
        optimized = sorted(target_data, key=lambda x: x['wait'] if is_urgent else x['crowd'])
        best, second = optimized[0], optimized[1]
        
        mode = "🚀 FASTEST PATH" if is_urgent else "🌈 COMFORT PATH"
        
        return f"""### RECOMMENDATION: {best['name']}
        
**Reasoning Matrix:**
| Factor | Status |
| :--- | :--- |
| **Logic Mode** | {mode} |
| **Queue Time** | {best['wait']} mins |
| **Crowd Level** | {best['crowd']}% |

**AI Insight:** Based on localized telemetry, this {category} is your optimal choice for the current {event['time_remaining']} window.

**Alternative:** {second['name']} (Slightly more congested)"""

    return "### 🔎 Specify Destination\nI need to know if you are looking for a **Gate**, **Food Stall**, or **Washroom** to calculate the optimal path for you."

if __name__ == '__main__':
    # Use environment port for deployment, default to 5000 for local dev
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
