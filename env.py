import random

class PowerCutEnv:
    def __init__(self, level="easy"):
        self.level = level
        self.zones = []
        self.total_supply = 0

    def reset(self):
        self.total_supply = 100

        self.zones = [
            {"name": "Hospital", "demand": 40, "priority": 5, "power": 0},
            {"name": "Residential", "demand": 30, "priority": 3, "power": 0},
            {"name": "Industry", "demand": 50, "priority": 2, "power": 0},
            {"name": "School", "demand": 20, "priority": 4, "power": 0},
        ]

        return self._get_state()

    def _get_state(self):
        return {
            "supply": self.total_supply,
            "zones": self.zones
        }

    def step(self, action):
        zone = self.zones[action]

        if self.total_supply <= 0:
            return self._get_state(), -10, True

        supply_given = min(10, self.total_supply)
        zone["power"] += supply_given
        self.total_supply -= supply_given

        # reward logic
        reward = zone["priority"] * supply_given

        done = self.total_supply <= 0

        return self._get_state(), reward, done