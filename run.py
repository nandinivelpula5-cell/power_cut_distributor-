import env as env_
import agent as agent_
import time

def print_state(state):
    print("\n" + "="*40)
    print(f"⚡ Available Supply: {state['supply']}")
    print("="*40)

    for i, z in enumerate(state["zones"]):
        print(f"[{i}] 🏢 {z['name']}")
        print(f"    Demand   : {z['demand']}")
        print(f"    Priority : {z['priority']}")
        print(f"    Supplied : {z['power']}")
        print("-"*40)


env = env_.PowerCutEnv(level="hard")
agent = agent_.SimpleAgent()

state = env.reset()
done = False
total_reward = 0

print("\n🚀 SMART POWER CUT MANAGEMENT SYSTEM")
print("="*50)

steps = 0
max_steps = 20

while not done and steps < max_steps:
    print_state(state)

    action = agent.choose_action(state)

    print(f"\n👉 AI chooses Zone: {action}")
    time.sleep(1)

    state, reward, done = env.step(action)

    total_reward += reward

    print(f"🎯 Reward: {reward}")
    print("="*50)

    steps += 1
    time.sleep(1)

print("\n✅ Simulation Finished")
print(f"🏆 Total Reward: {total_reward}")
print("="*50)