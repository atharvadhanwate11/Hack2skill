# Project Architecture

The Smart Stadium Flow Assistant is built on a decoupled architecture:

## 1. Frontend (The Fan Interface)
- **Single Page Application**: Uses Vanilla HTML/CSS/JS to keep the experience fast and responsive.
- **Dynamic Map**: Uses a relative coordinate system to map 'stalls' and 'gates' onto a 2D plane.
- **Polling Loop**: Every 5 seconds, the frontend polls the backend for new "sensor" data to update the UI without page refreshes.

## 2. Backend (The Intelligence Layer)
- **Flask REST API**: Handles data serving and AI orchestration.
- **Simulation Engine**: A Python module that adds "noise" and logic to the stadium state (e.g., if one gate is full, others might slowly fill up).
- **AI Orchestrator**: Bridges the user query with Google Gemini. It injects the *entire stadium state* into the context window, allowing the AI to make decisions based on real-time numbers rather than static text.

## 3. Data Model
- **Gates**: ID, Name, Coordinates, Crowd Level (%), Wait Time (min).
- **Stalls**: ID, Name, Coordinates, Crowd Level (%), Wait Time (min), Category (Food/Washroom).
- **Alerts**: Generated when thresholds are crossed (e.g., >80% crowd).
