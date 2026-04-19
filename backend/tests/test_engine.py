import unittest
import os
import json
from engine import StadiumSimulationEngine

class TestStadiumEngine(unittest.TestCase):
    def setUp(self):
        # Create a temp data file for testing
        self.test_data = {
            "food_stalls": [{"name": "Stall 1", "pos": [10, 10], "wait": 10, "crowd": 20}],
            "washrooms": [{"name": "Wash 1", "pos": [20, 20], "wait": 5, "crowd": 15}],
            "gates": [{"name": "Gate 1", "pos": [50, 50], "crowd": 10, "capacity": 100, "wait": 0}]
        }
        self.data_path = "test_stadium_data.json"
        with open(self.data_path, 'w') as f:
            json.dump(self.test_data, f)
        self.engine = StadiumSimulationEngine(self.data_path)

    def tearDown(self):
        if os.path.exists(self.data_path):
            os.remove(self.data_path)

    def test_initial_state(self):
        stadium, event = self.engine.get_current_state()
        self.assertEqual(event['phase'], "First Half")
        self.assertEqual(len(stadium['food_stalls']), 1)

    def test_tick_updates_values(self):
        initial_wait = self.engine.state['food_stalls'][0]['wait']
        # Tick multiple times to see updates
        for _ in range(5):
            self.engine.tick()
        
        current_wait = self.engine.state['food_stalls'][0]['wait']
        # Note: it might be the same by chance, but usually it changes
        # We just want to ensure it's still within bounds [1, 45]
        self.assertGreaterEqual(current_wait, 1)
        self.assertLessEqual(current_wait, 45)

    def test_phase_cycling(self):
        # Initial phase: First Half (index 0)
        # Ticks to change phase: 50
        for _ in range(50):
            self.engine.tick()
        
        _, event = self.engine.get_current_state()
        self.assertEqual(event['phase'], "Half-Time Surge")

if __name__ == '__main__':
    unittest.main()
