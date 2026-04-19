import unittest
import json
import os
import sys

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import mock_decision_engine

class TestAppLogic(unittest.TestCase):
    def setUp(self):
        self.mock_data = {
            "food_stalls": [
                {"name": "Burger Stand", "pos": [10, 10], "wait": 5, "crowd": 10},
                {"name": "Pizza Place", "pos": [90, 90], "wait": 50, "crowd": 80}
            ],
            "washrooms": [
                {"name": "Restroom A", "pos": [20, 20], "wait": 2, "crowd": 5},
                {"name": "Restroom B", "pos": [80, 80], "wait": 15, "crowd": 40}
            ],
            "gates": [
                {"name": "North Gate", "pos": [50, 50], "crowd": 30, "capacity": 100, "wait": 5}
            ]
        }
        self.mock_event = {"phase": "First Half"}
        self.user_pos = [12, 12]

    def test_mock_decision_engine_food(self):
        query = "Hungry for food"
        response = mock_decision_engine(query, self.user_pos, self.mock_data, self.mock_event)
        
        # It should recommend 'Burger Stand' since it has much lower wait and distance
        self.assertIn("Burger Stand", response)
        self.assertIn("OPTIMIZED", response)

    def test_mock_decision_engine_washroom(self):
        query = "Where is the nearest washroom?"
        response = mock_decision_engine(query, self.user_pos, self.mock_data, self.mock_event)
        self.assertIn("Restroom A", response)

    def test_mock_decision_engine_ambiguous(self):
        query = "What time is it?"
        response = mock_decision_engine(query, self.user_pos, self.mock_data, self.mock_event)
        
        # When query does not contain target keywords, it asks for clarification
        self.assertIn("Please specify", response)

if __name__ == '__main__':
    unittest.main()
