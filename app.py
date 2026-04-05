import streamlit as st
import time

# ---------------- ENV ----------------
class PowerCutEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.total_supply = 100
        self.zones = [
            {"name": "Hospital", "demand": 40, "priority": 5, "power": 0},
            {"name": "Residential", "demand": 30, "priority": 3, "power": 0},
            {"name": "Industry", "demand": 50, "priority": 2, "power": 0},
            {"name": "School", "demand": 20, "priority": 4, "power": 0},
        ]

    def step(self, action):
        zone = self.zones[action]

        if self.total_supply <= 0:
            return -10

        supply = min(10, self.total_supply)
        zone["power"] += supply
        self.total_supply -= supply

        reward = zone["priority"] * supply
        return reward


# ---------------- AGENT ----------------
class SimpleAgent:
    def choose_action(self, zones):
        best = -1
        idx = 0

        for i, z in enumerate(zones):
            if z["power"] < z["demand"] and z["priority"] > best:
                best = z["priority"]
                idx = i

        return idx


# ---------------- UI ----------------
st.set_page_config(page_title="⚡ Power Manager", layout="wide")

st.title("⚡ Smart Power Cut Management System")

# session state
if "env" not in st.session_state:
    st.session_state.env = PowerCutEnv()
    st.session_state.agent = SimpleAgent()
    st.session_state.score = 0

env = st.session_state.env

# supply display
st.subheader(f"🔋 Available Supply: {env.total_supply}")

# zone display
cols = st.columns(len(env.zones))

for i, zone in enumerate(env.zones):
    with cols[i]:
        st.markdown(f"### 🏢 {zone['name']}")
        st.write(f"Demand: {zone['demand']}")
        st.write(f"Priority: {zone['priority']}")

        progress = zone["power"] / zone["demand"]
        st.progress(min(progress, 1.0))

        st.write(f"Supplied: {zone['power']}")

        if st.button(f"⚡ Supply {zone['name']}", key=i):
            reward = env.step(i)
            st.session_state.score += reward
            st.rerun()

# AI button
st.markdown("---")
if st.button("🤖 Auto Allocate (AI)"):
    action = st.session_state.agent.choose_action(env.zones)
    reward = env.step(action)
    st.session_state.score += reward
    st.rerun()

# reset button
if st.button("🔄 Reset Simulation"):
    st.session_state.env = PowerCutEnv()
    st.session_state.score = 0
    st.rerun()

# score
st.markdown("---")
st.subheader(f"🏆 Total Score: {st.session_state.score}")