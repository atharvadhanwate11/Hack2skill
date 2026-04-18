import random
import json
import os

class StadiumSimulationEngine:
    """
    Handles the real-time simulation logic for crowd dynamics and facility status.
    Decoupled from the API layer for scalability and testing.
    """
    def __init__(self, data_path):
        self.data_path = data_path
        self.stadium_data = self._load_initial_data()
        self.event_status = {
            "status": "Match in Progress",
            "time_remaining": "20' to Half-Time",
            "score": "2 - 1"
        }

    def _load_initial_data(self):
        with open(self.data_path, 'r') as f:
            return json.load(f)

    def tick(self):
        """Advances the simulation by one state."""
        # 1. Update Game Clock
        if random.random() > 0.7:
            try:
                mins = int(self.event_status['time_remaining'].split("'")[0])
                if mins > 1:
                    self.event_status['time_remaining'] = f"{mins - 1}' to Half-Time"
            except: pass

        # 2. Update Facility Metrics
        for category in ['gates', 'food_stalls', 'washrooms']:
            for item in self.stadium_data[category]:
                # Dynamic fluctuation based on simple crowd-flow simulation
                item['crowd'] = max(5, min(100, item['crowd'] + random.randint(-4, 4)))
                item['wait'] = max(1, min(45, item['wait'] + random.randint(-1, 1)))
        
        return self.stadium_data, self.event_status

    def get_current_state(self):
        return self.stadium_data, self.event_status
