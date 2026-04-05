from env import PowerCutEnv

env = PowerCutEnv()

# test all levels
levels = ["easy", "medium", "hard"]

for level in levels:
    env.load_task(level)
    obs = env.reset()

    done = False
    total_reward = 0

    while not done:
        # simple greedy: choose highest priority zone
        priorities = [z["priority"] for z in env.zones]
        action = priorities.index(max(priorities))

        result = env.step(action)
        total_reward += result["reward"]
        done = result["done"]

    print(f"{level.upper()} SCORE:", total_reward)
