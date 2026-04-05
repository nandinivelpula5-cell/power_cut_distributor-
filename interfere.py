from env import PowerCutEnv
import random

random.seed(42)

env = PowerCutEnv()

levels = ["easy", "medium", "hard"]

for level in levels:
    env.load_task(level)
    obs = env.reset()

    done = False

    while not done:
        priorities = [z["priority"] for z in env.zones]
        action = priorities.index(max(priorities))

        result = env.step(action)
        done = result["done"]

    score = env.get_score()
    print(f"{level.upper()} SCORE:", score)
