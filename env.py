import random

class PowerCutEnv:
    def __init__(self, level="easy"):
        self.level = level
        self.zones = []
        self.total_supply = 0

    def reset(self):
    self.supply = 100
    self.zones = [
        {"name": "Hospital", "demand": 40, "priority": 4, "power": 0},
        {"name": "Residential", "demand": 50, "priority": 2, "power": 0},
        {"name": "Industrial", "demand": 30, "priority": 1, "power": 0}
    ]

    return {
        "observation": self.state(),
        "info": {}
    }

    

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
