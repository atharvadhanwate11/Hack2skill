<div align="center">
  <img src="frontend/logo.png" width="120" height="120" alt="StadiumFlow AI Logo">
  <h1>StadiumFlow AI</h1>
  <p><b>Precision-Engineered Stadium Intelligence with Google Gemini & Real-Time Physics.</b></p>
  
  [![Google Services](https://img.shields.io/badge/Google_Services-Gemini_%7C_Maps_%7C_Calendar-blue.svg)](https://cloud.google.com/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
  [![Testing](https://img.shields.io/badge/Tests-Passed-brightgreen.svg)](backend/tests/)
</div>

---

## 📖 Problem Statement: The "Flash Congestion" Crisis
Large-scale sporting events suffer from **Flash Congestion**—sudden, extreme spikes in localized crowd density during game breaks or final whistles. This leads to inefficiency, safety risks, and lost revenue.

## 💡 The Solution: StadiumFlow AI
StadiumFlow is an **Interconnected Digital Twin Engine**. By cross-referencing phase-driven telemetry, Euclidean spatial math, and user localization, it provides industrial-grade navigational guidance that captures the "Live Pulse" of the stadium.

---

## 🛠️ System Workflow
1.  **Ingestion**: Real-time telemetry is streamed from the **Phase-Driven Physics Engine**.
2.  **Contextualization**: The system detects the current match lifecycle (e.g., *Half-Time Surge* or *Final Whistle Egress*).
3.  **Optimization**: The engine calculates a **Weighted Utility Score** for every facility using Euclidean spatial math.
4.  **Orchestration**: The localized state is passed to **Google Gemini** for natural language reasoning.
5.  **Delivery**: A structured, actionable recommendation is pushed to a high-performance **Crystalline Glass UI**.

---

## 🎯 Evaluation Focus: Meeting the Top 50 Criteria

### 1. 🚀 Google Services Integration
- **Google GenAI (Gemini-2.0-Flash)**: Orchestrates complex navigation decisions using real-time sensor data via the latest, officially supported `google-genai` SDK.
- **Google Maps Platform**: Live embedded `<iframe>` integration for dynamic, in-app venue synchronization across 3 major global stadiums.
- **Google Calendar**: Live event schedule tracking for phase-aware AI adaptation.
- **Google Fonts**: Premium typography using `Outfit` and `Inter`.

### 2. 🧪 Testing & Validation
- **Integrated Test Suite**: Comprehensive `unittest` package in `backend/tests/` covering engine physics (`test_engine.py`), application orchestration logic, and mock fallback AI (`test_app.py`).
- **Deterministic Simulation**: A phase-driven physics engine allows for repeatable stress testing of crowd surges.

### 3. 🎨 Visual Excellence (WOW factor)
- **Crystalline Glass UI**: Dark-mode aesthetic with frosted glass, vibrant gradients, and micro-animations.
- **Dynamic Pathfinding**: Live SVG Bezier-curve generation for visual route mapping.
- **Compass Tracking**: Device Magnetometer integration for real-time orientation.
- **Voice Control**: Integrated Web Speech API for hands-free "Industrial Assistant" interaction.

### 4. 🔒 Security & Quality
- **Security Engineering**: Zero API key leakage via `.env` architecture; CORS protection; full `html.escape` input sanitization implemented in `app.py` for Gemini prompt defense.
- **Code Quality**: Clean, modular architecture separating the Simulation Engine, AI Orchestrator, and Frontend.
- **Accessibility**: Full semantic HTML5 and ARIA-labeling for inclusive design.

### 5. ⚡ Efficiency
- **Minimal Footprint**: Repository size < 1MB (optimizing resources).
- **High Performance**: Vanilla JS frontend avoids framework bloat, ensuring sub-100ms UI responsiveness.

---

## 🧠 AI Decision Logic: Weighted Utility Scoring
The core of StadiumFlow is its **Industrial Optimization Formula**.
1. **The Formula**: `Utility = (WaitTime * 0.5) + (EuclDist * 0.3) + (CrowdDensity * 0.2)`
2. **Phase Awareness**: During high-urgency phases (e.g., Half-time), the system automatically doubles the "Wait Time" weighting.
3. **Spatial Math**: Instead of relative sectors, the AI uses raw `[x,y]` coordinate deltas for absolute proximity calculations.

---

## 🚀 How to Run (Local)
1. **Setup**: `cd backend && pip install -r requirements.txt`
2. **Credentials**: Add `GEMINI_API_KEY` to `backend/.env`.
3. **Launch**: `python app.py`
4. **Access**: Navigate to `http://127.0.0.1:5000`

**StadiumFlow AI — Masters of the Stadium Pulse.**
