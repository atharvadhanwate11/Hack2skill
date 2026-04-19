# 🏆 Judge's Q&A: Master your Submission

Use this "Cheat Sheet" to answer technical questions during your hackathon presentation.

### Q1: "How does the AI Assistant actually make decisions?"
**Answer:** We use a **Contextual Weighting Algorithm**. The system has two modes:
1.  **Efficiency Mode (High Urgency)**: Activated when the game clock is near a restart. Weights are shifted to prioritize "Minimum Wait Time."
2.  **Comfort Mode (Low Urgency)**: Activated during active play. Weights are shifted to prioritize "Shortest Distance" and "Lowest Crowd Density."

### Q2: "Is this using real GPS?"
**Answer:** Yes. The frontend utilizes the browser's **Geolocation API** (`navigator.geolocation.watchPosition`). We created a **Geometric Scaling Engine** that translates the delta in Latitude/Longitude into movement on our Stadium Grid (0-100%).

### Q3: "What happens if the Gemini API fails or there's no internet?"
**Answer:** We've built **API Failure Resilience**. The system detects the failure and instantly switches to a **Deterministic Decision-Tree (Mock AI)**. This ensures the fans still get structured navigational advice based on the local simulation data, even if the cloud is offline.

### Q4: "Where is the data coming from?"
**Answer:** It’s a **Digital Twin** simulation. Our backend `engine.py` generates synthetic telemetry that mimics IoT sensors. It uses a **Gaussian Walk** algorithm so crowd levels fluctuate realistically over time, rather than just being static numbers.

### Q5: "How is this scalable?"
**Answer:** We've used a **Modular Architecture**. The Simulation Engine is completely decoupled from the API. In a production environment, we would simply swap the `engine.py` module with a real-time WebSocket feed from physical stadium sensors.

### Q6: "Why did you use Vanilla JavaScript instead of a big framework like React?"
**Answer:** For **Performance & Lightweight Footprint**. In a stadium with 50,000 people, bandwidth is limited. Our app is **<1MB**, loads instantly, and has zero heavy external dependencies, making it more resilient on congested stadium Wi-Fi.

### Q7: "How did you integrate Google Services beyond just a chatbot?"
**Answer:** We leverage a **Google Ecosystem Triumvirate**:
- **Cognitive Layer**: Gemini 1.5 Flash for industrial-grade logic orchestration.
- **Spatial Layer**: Google Maps Platform for venue synchronization and navigation-handoff.
- **Workflow Layer**: Google Calendar logic for phase-aware adaptive scaling.
- **Interaction Layer**: Integrated Voice Recognition (via Web Speech API) for a smart, hands-free assistant experience.
