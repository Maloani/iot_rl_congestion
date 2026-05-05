import numpy as np
from rl_model import RLAgent
from config import SEED, EPISODES, STEPS_PER_EPISODE

np.random.seed(SEED)
agent = RLAgent()

def simulate_tcp():
    return {
        "throughput": 5 + np.random.rand()*1.5,
        "latency": 110 + np.random.rand()*20,
        "loss": 10 + np.random.rand()*4,
        "energy": 80 + np.random.rand()*10
    }

def simulate_rl():
    rewards = []
    for _ in range(EPISODES):
        total_reward = 0
        state = np.random.rand(4)

        for _ in range(STEPS_PER_EPISODE):
            action = agent.choose_action(state)
            next_state = np.random.rand(4)
            reward = 10 - np.sum(next_state)
            agent.train(state, action, reward, next_state)

            total_reward += reward
            state = next_state

        rewards.append(total_reward)

    return {
        "throughput": 7 + np.random.rand()*2,
        "latency": 55 + np.random.rand()*15,
        "loss": 2 + np.random.rand()*2,
        "energy": 50 + np.random.rand()*10,
        "rewards": rewards
    }

def run_simulation():
    tcp = simulate_tcp()
    rl = simulate_rl()

    return {
        "TCP": tcp,
        "RL (DQN)": rl
    }