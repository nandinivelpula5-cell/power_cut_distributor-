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

    if self.supply >= zone["demand"] and zone["power"] == 0:
        zone["power"] = zone["demand"]
        self.supply -= zone["demand"]
        reward += zone["priority"] * 10
    else:
        reward -= 5

    done = self.supply <= 0 or all(z["power"] > 0 for z in self.zones)

    return {
        "observation": self.state(),
        "reward": reward,
        "done": done,
        "info": {}
    }
        done = self.total_supply <= 0

        return self._get_state(), reward, done
