from typing import Dict
import random

class PowerCutEnv:

    def __init__(self):
        self.supply = 0
        self.zones = []

    def load_task(self, difficulty="easy"):
        if difficulty == "easy":
            self.supply = 100
            self.zones = [
                {"name": "Hospital", "demand": 30, "priority": 5, "power": 0},
                {"name": "Home", "demand": 20, "priority": 3, "power": 0},
            ]

        elif difficulty == "medium":
            self.supply = 80
            self.zones = [
                {"name": "Hospital", "demand": 40, "priority": 5, "power": 0},
                {"name": "Residential", "demand": 30, "priority": 3, "power": 0},
                {"name": "Industry", "demand": 30, "priority": 1, "power": 0},
            ]

        elif difficulty == "hard":
            random.seed(42)
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
        reward = 0.0
        done = False

        if action < 0 or action >= len(self.zones):
            return {
                "observation": self.state(),
                "reward": 0.0,
                "done": True,
                "info": {}
            }

        zone = self.zones[action]
        max_priority = 5

        if self.supply >= zone["demand"] and zone["power"] == 0:
            zone["power"] = zone["demand"]
            self.supply -= zone["demand"]
            reward += zone["priority"] / max_priority

        elif self.supply > 0 and zone["power"] == 0:
            zone["power"] = self.supply
            reward += (zone["priority"] / max_priority) * 0.5
            self.supply = 0

        else:
            reward -= 0.2

        reward = max(0.0, min(1.0, reward))

        done = self.supply <= 0 or all(z["power"] > 0 for z in self.zones)

        return {
            "observation": self.state(),
            "reward": float(reward),
            "done": done,
            "info": {}
        }

    def get_score(self) -> float:
        total = sum(z["power"] for z in self.zones)
        demand = sum(z["demand"] for z in self.zones)

        return round(total / demand, 2) if demand > 0 else 0.0