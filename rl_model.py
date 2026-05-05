import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim)
        )

    def forward(self, x):
        return self.fc(x)

class RLAgent:
    def __init__(self):
        self.model = DQN(4, 3)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
        self.gamma = 0.9

    def choose_action(self, state):
        if random.random() < 0.2:
            return random.randint(0, 2)

        state = torch.FloatTensor(state)
        q_values = self.model(state)
        return torch.argmax(q_values).item()

    def train(self, state, action, reward, next_state):
        state = torch.FloatTensor(state)
        next_state = torch.FloatTensor(next_state)

        q_values = self.model(state)
        next_q_values = self.model(next_state)

        target = q_values.clone()
        target[action] = reward + self.gamma * torch.max(next_q_values)

        loss = self.criterion(q_values, target.detach())

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()