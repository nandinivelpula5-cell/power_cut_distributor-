from typing import Dict, List
import random

class PowerCutEnv:

    def __init__(self):
        self.supply = 0
        self.zones = []

    def load_task(self, difficulty="easy"):
        if difficulty == "easy":
            self.supply = 100
            self.zones = [
                {"name": "Hospital", "demand": 30, "priority": 4, "power": 0},
                {"name": "Home", "demand": 20, "priority": 2, "power": 0},
            ]

        elif difficulty == "medium":
            self.supply = 80
            self.zones = [
                {"name": "Hospital", "demand": 40, "priority": 5, "power": 0},
                {"name": "Residential", "demand": 30, "priority": 3, "power": 0},
                {"name": "Industry", "demand": 30, "priority": 1, "power": 0},
            ]

        elif difficulty == "hard":
            self.supply = random.randint(50, 100)
            self.zones = [
                {"name": "Hospital", "demand": random.randint(30, 50), "priority": 5, "power": 0},
                {"name": "City", "demand": random.randint(20, 40), "priority": 3, "power": 0},
                {"name": "Factory", "demand": random.randint(10, 30), "priority": 1, "power": 0},
            ]

    def state(self) -> Dict:
        return {
            "supply": self.supply,
            "zones": self.zones
        }

    def reset(self):
        if not self.zones:
            self.load_task("medium")

        for z in self.zones:
            z["power"] = 0

        return {
            "observation": self.state(),
            "info": {}
        }

    def step(self, action: int):
        reward = 0
        done = False

        if action < 0 or action >= len(self.zones):
            return {
                "observation": self.state(),
                "reward": -10,
                "done": True,
                "info": {}
            }

        zone = self.zones[action]

        # full allocation
        if self.supply >= zone["demand"] and zone["power"] == 0:
            zone["power"] = zone["demand"]
            self.supply -= zone["demand"]
            reward += zone["priority"] * 10

        # partial allocation
        elif self.supply > 0 and zone["power"] == 0:
            zone["power"] = self.supply
            reward += zone["priority"] * 5
            self.supply = 0

        else:
            reward -= 5

        done = self.supply <= 0 or all(z["power"] > 0 for z in self.zones)

        return {
            "observation": self.state(),
            "reward": reward,
            "done": done,
            "info": {}
        }
