from typing import Dict, List
import random

class PowerCutEnv:

    def __init__(self):
        self.supply = 0
        self.zones = []

    # ---------------- TASKS ----------------
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
            random.seed(42)  # reproducible
            self.supply = random.randint(50, 100)
            self.zones = [
                {"name": "Hospital", "demand": random.randint(30, 50), "priority": 5, "power": 0},
                {"name": "City", "demand": random.randint(20, 40), "priority": 3, "power": 0},
                {"name": "Factory", "demand": random.randint(10, 30), "priority": 1, "power": 0},
            ]

    # ---------------- STATE ----------------
    def state(self) -> Dict:
        return {
            "supply": self.supply,
            "zones": self.zones
        }

    # ---------------- RESET ----------------
    def reset(self):
        if not self.zones:
            self.load_task("medium")

        for z in self.zones:
            z["power"] = 0

        return {
            "observation": self.state(),
            "info": {}
        }

    # ---------------- STEP ----------------
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

        # Full allocation
        if self.supply >= zone["demand"] and zone["power"] == 0:
            zone["power"] = zone["demand"]
            self.supply -= zone["demand"]
            reward += zone["priority"] / max_priority  # max 1.0

        # Partial allocation
        elif self.supply > 0 and zone["power"] == 0:
            allocated = self.supply
            zone["power"] = allocated
            reward += (zone["priority"] / max_priority) * 0.5
            self.supply = 0

        # Invalid / repeat action
        else:
            reward -= 0.2

        # Clamp reward between 0 and 1
        reward = max(0.0, min(1.0, reward))

        done = self.supply <= 0 or all(z["power"] > 0 for z in self.zones)

        return {
            "observation": self.state(),
            "reward": float(reward),
            "done": done,
            "info": {}
        }

    # ---------------- SCORING ----------------
    def get_score(self) -> float:
        total_power = sum(z["power"] for z in self.zones)
        total_demand = sum(z["demand"] for z in self.zones)

        if total_demand == 0:
            return 0.0

        return round(total_power / total_demand, 2)
