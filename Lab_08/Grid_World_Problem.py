import numpy as np

rows = 4
cols = 3
gamma = 0.9  # Discount factor

def get_reward(state):
    if state == 11:
        return 1
    elif state == 10:
        return -1
    else:
        return -0.04

actions = ['up', 'down', 'left', 'right']

P_intended = 0.8
P_orthogonal = 0.1

V = np.zeros(rows * cols)

def get_neighbors(state):
    row, col = divmod(state, cols)
    neighbors = {'up': state, 'down': state, 'left': state, 'right': state}
    if row > 0: neighbors['up'] = state - cols
    if row < rows - 1: neighbors['down'] = state + cols
    if col > 0: neighbors['left'] = state - 1
    if col < cols - 1: neighbors['right'] = state + 1
    return neighbors

def bellman_update(V):
    new_V = np.copy(V)
    for state in range(rows * cols):
        if state in [10, 11]:  # Terminal states
            continue
        action_values = []
        for action in actions:
            neighbors = get_neighbors(state)
            intended_state = neighbors[action]
            orthogonal_states = [
                neighbors[a] for a in actions if a != action
            ]
            expected_value = P_intended * (get_reward(intended_state) + gamma * V[intended_state])
            for ortho_state in orthogonal_states:
                expected_value += P_orthogonal * (get_reward(ortho_state) + gamma * V[ortho_state])
            action_values.append(expected_value)
        new_V[state] = max(action_values)
    return new_V

tolerance = 1e-6
delta = float('inf')

while delta > tolerance:
    delta = 0
    new_V = bellman_update(V)
    delta = np.max(np.abs(new_V - V))
    V = np.copy(new_V)

print("Value function after value iteration:")
for i in range(rows):
    print(V[i * cols:(i + 1) * cols])
