class SimpleAgent:
    def choose_action(self, state):
        zones = state["zones"]

        # choose zone with highest priority but not fully powered
        best_index = -1
        best_priority = -1

        for i, z in enumerate(zones):
            if z["power"] < z["demand"]:  # needs power
                if z["priority"] > best_priority:
                    best_priority = z["priority"]
                    best_index = i

        return best_index if best_index != -1 else 0