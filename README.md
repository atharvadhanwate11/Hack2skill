# 🏟️ StadiumFlow: Real-Time Optimization Engine

**Empowering massive venues with data-driven flow control and AI-guided attendee navigation.**

---

## 📖 Problem Statement: The "Flash Congestion" Crisis
Large-scale sporting events suffer from **Flash Congestion**—sudden, extreme spikes in localized crowd density during game breaks or final whistles. This leads to:
- **Inefficiency**: Attendees spend 30%+ of their time in queues rather than the seats.
- **Safety Risks**: Bottle-necks at gates increase evacuation risks.
- **Lost Revenue**: Long food stall queues lead to abandoned purchases.

## 💡 The Solution: StadiumFlow
StadiumFlow is not just a digital map; it is a **Decision-Driven Optimization Engine**. By cross-referencing live sensor data (simulated), event timing, and user location, it provides high-precision navigational guidance that balances venue throughput with attendee comfort.

---

## 🛠️ System Workflow
1.  **Ingestion**: Real-time telemetry (Crowd %, Wait Times) is streamed from the **StadiumSimulationEngine**.
2.  **Contextualization**: Attendee location and current match status (clock/score) are appended to the data state.
3.  **Optimization**: The **Decision-Path Engine** assigns weights based on urgency (Game-play vs. Break).
4.  **Orchestration**: The localized state is passed to **Google Gemini** for natural language reasoning.
5.  **Delivery**: A structured, actionable recommendation is pushed to the client-side dashboard.

---

## ✨ Key Features (System-Grade)
- **🛰️ Dynamic Flow Visualization**: High-fidelity architectural map with green/yellow/red congestion heatmapping.
- **✨ Decision-Path AI**: Google Gemini-powered engine that calculates "Time-Impact" for every recommendation.
- **🔵 Live "Blue Dot" Tracking**: Real-time attendee localization using browser Geolocation and Motion Scaling.
- **🧭 Compass-Heading Arrow**: Device Magnetometer integration to show exactly which way the user is facing.
- **🛣️ Dynamic Pathfinding Lines**: Live Bezier-curve generation to visually draw a navigation path from user to destination.
- **🕒 Event-Context Awareness**: High-urgency mode that shifts navigation logic from "Comfort" to "Speed" during game-restart windows.
- **🎨 Crystalline Glass UI**: Sky-Blue and Frosted-White "Cloud SaaS" aesthetic for maximum readability.

---

## 🧠 AI Decision Logic
The core of StadiumFlow is its **Contextual Weighting Algorithm**.
1. **Urgency Assessment**: The system analyzes the "Event Status." If a restart is within 5 minutes, it moves to **High-Urgency Mode**.
2. **Path Scoring**: It evaluates facilities using a composite score: 
   `Score = (Normalized Wait Time * W1) + (Crowd Density Index * W2) + (Proximity Factor * W3)`
3. **Weight Shift**: In High-Urgency, `W1` (Efficiency) becomes the dominant factor. In Low-Urgency, `W2` (Comfort) is prioritized.

---

## 🤖 Interaction Example
**User Query**: "Where should I go for food quickly?"

**StadiumFlow Response**:
- **Recommendation**: Stall B (North Concourse)
- **Why**: 
    - **Wait Time**: Only 3 minutes (Lowest in current zone).
    - **Crowd**: 15% density (Low).
    - **Event Timing**: 4 minutes remaining in quarter (Optimal window).
- **Alternative Option**: Stall D (Slightly further but has zero queue).
- **Estimated Time Impact**: Saves approx. 12 minutes compared to the nearest facility (Stall A).

---

## 🛠️ Tech Stack & Architecture
- **Engine**: Python (Flask) with a modular Simulation Data Layer.
- **Intelligence**: Google Gemini-1.5-Flash (LLM Orchestration).
- **Frontend**: High-Performance Vanilla JS/CSS3 (Aesthetic: Industrial Glassmorphism).
- **Simulation**: High-fidelity fluctuation engine for real-time state management.

---

## ☁️ Google Ecosystem Integration
- **Google Gemini (Flash 1.5)**: Acts as the "Cognitive Layer," transforming raw facility telemetry into reasoned, structured advice.
- **Firebase (Conceptual)**: Architected to use Firebase Realtime Database for instantaneous state synchronization across 50,000+ simultaneous users.
- **Google Maps Platform**: Future-mapped for high-precision indoor polyline routing and geofencing around stadium gates.

---

## 🛡️ Trust & Evaluation Areas

### 🔒 Security & Privacy
- **Environment Isolation**: API keys are managed exclusively via `python-dotenv` and excluded from source control.
- **Sanitization**: Chat inputs are sanitized before being passed to the Generative model.
- **Privacy by Design**: No personal PII is stored; location data is relative, not absolute GPS.

### ♿ Accessibility
- **Chroma Coding**: Every status is color-coded (Red/Yellow/Green) for at-a-glance accessibility.
- **Predictive Layout**: High-contrast, high-readability typography (Outfit/Inter).
- **One-Tap Interaction**: Minimal interaction steps to reach critical optimization data.

### 🧪 Testing & Edge Cases
- **Stress Simulation**: Internal logic tests behavior at "100% Crowd" saturation to ensure recommendation diversity.
- **API Failure Resilience**: A robust deterministic Decision-Tree fallback ensures the system functions even if Google APIs are unavailable.
- **Empty State Handling**: Safety logic prevents UI fragmentation if sensor data is partially missing.

### ⚡ Efficiency
- **Execution**: Lightweight footprint (<1MB repository).
- **Performance**: Zero heavy client-side libraries; optimized for low-latency mobile browsers.

### 📝 Operational Assumptions
- **Telemetry**: Real-time facility data is simulated via a Gaussian fluctuation engine for the prototype.
- **Localization**: User location is derived via Sector/Section geofencing rather than high-battery GPS.
- **Connectivity**: System assumes stable 4G/5G/Stadium Wi-Fi for real-time AI orchestration.

---

## 🏗️ Architectural Decisions
### Why a "Digital Twin" Simulation?
A common question is: *"Why not use a public API for stadium crowd data?"*
- **Privacy & Security**: Real-time internal crowd telemetry (IoT sensor data) is proprietary and highly sensitive. No public API provides live gate-level density for free.
- **Reliability (Deterministic Testing)**: By building a **Gaussian Simulation Engine**, we can test our AI's decision-making under "Stress Scenarios" (90%+ congestion) that wouldn't be available via a real-world API during a 3-minute hackathon demo.
- **Production Path**: The system is built with an **Interchangeable Provider Pattern**. The `engine.py` module can be swapped with a live Google Maps Indoor or IoT WebSocket hook without changing a single line of AI logic.

---

## 🔌 External API Roadmap
The system is architected to "Hook" into the following public streams:
- **[TheSportsDB](https://www.thesportsdb.com/)**: For live match scoring events that trigger pre-emptive surge management.
- **[OpenWeather API](https://openweathermap.org/)**: To dynamically redirect fans to "Covered" concourses during sudden weather events.
- **[Google Maps Indoor API](https://developers.google.com/maps/documentation/gaming/concepts/indoor-mapping)**: For transition from schematic grids to high-fidelity architectural polylines.

---
1. **Setup**: `cd backend && pip install -r requirements.txt`
2. **Credentials**: Add `GEMINI_API_KEY` to `backend/.env` (optional fallback included).
3. **Launch**: `python app.py`
4. **Access**: Navigate to `http://127.0.0.1:5000`

---

## 🔮 Future Scope
- **Google Maps Indoor**: Transitioning from relative grids to actual high-precision floor plans.
- **Predictive Surge Logic**: Using ML to predict bathroom rushes 5 minutes before they happen.
- **Ticketing Integration**: Direct-to-seat turnstile optimization.

**StadiumFlow — Masters of the Stadium Pulse.**
