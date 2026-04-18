import json
import random
import time

class StadiumSimulationEngine:
    def __init__(self, data_path):
        self.data_path = data_path
        with open(data_path, 'r') as f:
            self.state = json.load(f)
        
        self.event_phases = ["First Half", "Half-Time Surge", "Second Half", "Final Whistle Egress"]
        self.phase_index = 0
        self.tick_count = 0

    def get_current_state(self):
        # Calculate event context
        event = {
            "phase": self.event_phases[self.phase_index],
            "score": "2 - 1",
            "time_remaining": f"{45 - (self.tick_count % 45)}' left" if self.phase_index % 2 == 0 else "SURGE ACTIVE"
        }
        return self.state, event

    def tick(self):
        self.tick_count += 1
        
        # Cycle through phases every 50 ticks for demo purposes
        if self.tick_count % 50 == 0:
            self.phase_index = (self.phase_index + 1) % len(self.event_phases)
        
        current_phase = self.event_phases[self.phase_index]
        
        # --- PHASE-DRIVEN PHYSICS ENGINE ---
        for stall in self.state['food_stalls']:
            # Half-time makes people hungry (Surge)
            multiplier = 4.0 if current_phase == "Half-Time Surge" else 1.0
            stall['wait'] = max(1, min(45, stall['wait'] + random.randint(-2, 3) * multiplier))
            stall['crowd'] = max(5, min(100, stall['crowd'] + random.randint(-5, 8) * multiplier))

        for wash in self.state['washrooms']:
            # Washrooms burst during breaks
            multiplier = 5.0 if current_phase == "Half-Time Surge" else 0.5
            wash['wait'] = max(1, min(20, wash['wait'] + random.randint(-1, 2) * multiplier))
            wash['crowd'] = max(10, min(100, wash['crowd'] + random.randint(-5, 10) * multiplier))

        for gate in self.state['gates']:
            # Gates explode at the end
            multiplier = 6.0 if current_phase == "Final Whistle Egress" else 0.2
            gate['crowd'] = max(5, min(100, gate['crowd'] + random.randint(-2, 5) * multiplier))
            # Wait time at gates is modeled by Crowd / Capacity
            gate['wait'] = int((gate['crowd'] / gate['capacity']) * 60)

        return self.get_current_state()
