<div align="center">
  <img src="frontend/logo.png" width="120" height="120" alt="StadiumFlow AI Logo">
  <h1>StadiumFlow AI</h1>
  <p><b>Mastering the Pulse of Massive Venues with Real-Time Data & Cognitive Intelligence.</b></p>
</div>

---

## 📖 Problem Statement: The "Flash Congestion" Crisis
Large-scale sporting events suffer from **Flash Congestion**—sudden, extreme spikes in localized crowd density during game breaks or final whistles. This leads to:
- **Inefficiency**: Attendees spend 30%+ of their time in queues rather than the seats.
- **Safety Risks**: Bottle-necks at gates increase evacuation risks.
- **Lost Revenue**: Long food stall queues lead to abandoned purchases.

## 💡 The Solution: StadiumFlow AI
StadiumFlow is an **Interconnected Digital Twin Engine**. By cross-referencing phase-driven telemetry, Euclidean spatial math, and user localization, it provides industrial-grade navigational guidance that captures the "Live Pulse" of the stadium.

---

## 🛠️ System Workflow
1.  **Ingestion**: Real-time telemetry is streamed from the **Phase-Driven Physics Engine**.
2.  **Contextualization**: The system detects the current match lifecycle (e.g., *Half-Time Surge* or *Final Whistle Egress*).
3.  **Optimization**: The engine calculates a **Weighted Utility Score** for every facility using Euclidean spatial math.
4.  **Orchestration**: The localized state is passed to **Google Gemini** for natural language reasoning.
5.  **Delivery**: A structured, actionable recommendation is pushed to the client-side dashboard.

---

## ✨ Key Features (System-Grade)
- **🛰️ Phase-Driven Simulation**: Real-world crowd 'waves' (Half-time bursts, Exit surges) simulated via a dedicated physics layer.
- **📊 Weighted Utility AI**: Advanced scoring model: `(Wait * 0.5) + (Dist * 0.3) + (Crowd * 0.2)`.
- **🔵 Euclidean Spatial Tracking**: Direct math-based proximity calculation between user position and facility coordinates.
- **🧭 Compass-Heading Arrow**: Device Magnetometer integration to show exactly which way the user is facing.
- **🛣️ Dynamic Pathfinding Lines**: Live Bezier-curve generation to visually draw a navigation path from user to destination.
- **🕒 Event-Context Awareness**: AI automatically detects the match clock to shift redirection logic from "Comfort" to "High-Capacity Egress".
- **🎨 Crystalline Glass UI**: Sky-Blue and Frosted-White "Cloud SaaS" aesthetic for maximum readability.

---

## 🧠 AI Decision Logic: Weighted Utility Scoring
The core of StadiumFlow is its **Industrial Optimization Formula**.
1. **The Formula**: `Utility = (WaitTime * 0.5) + (EuclideanDistance * 0.3) + (CrowdDensity * 0.2)`
2. **Phase Awareness**: During high-urgency phases (e.g., Half-time), the system automatically doubles the "Wait Time" weighting to ensure attendees return to their seats before the whistle.
3. **Spatial Math**: Instead of relative sectors, the AI uses raw `[x,y]` coordinate deltas to calculate absolute proximity.

---

## 🛠️ Tech Stack & Architecture
- **Engine**: Python (Flask) with a Phase-State Physics Layer.
- **Intelligence**: Google Gemini-1.5-Flash (Industrial Logic Orchestration).
- **Frontend**: High-Performance Vanilla JS (Aesthetic: Crystalline Frosted Glass).
- **Spatial Layer**: SVG Bezier-Path Engine for dynamic route mapping.

---

## 🏗️ Architectural Decisions
### Why a "Digital Twin" Simulation?
A common question is: *"Why not use a public API for stadium crowd data?"*
- **Privacy & Security**: Real-time crowd telemetry is proprietary data. No public API provides live gate-level density.
- **Reliability**: By building a **Phase-Driven Physics Engine**, we can simulate 400% surges (stress tests) that would be impossible to trigger during a live demo.
- **Scaling**: The system uses an **Interchangeable Provider Pattern**: swap `engine.py` with an IoT WebSocket hook to move to production.

---

## 🚀 How to Run (Local)
1. **Setup**: `cd backend && pip install -r requirements.txt`
2. **Credentials**: Add `GEMINI_API_KEY` to `backend/.env`.
3. **Launch**: `python app.py`
4. **Access**: Navigate to `http://127.0.0.1:5000`

**StadiumFlow AI — Masters of the Stadium Pulse.**
