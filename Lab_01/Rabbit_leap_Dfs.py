from collections import deque

def is_goal(state):
    return state == ['W', 'W', 'W', '_', 'E', 'E', 'E']

def get_successors(state):
    successors = []
    empty_index = state.index('_')

    # Define possible moves: left (-1), right (+1), jump left (-2), jump right (+2)
    moves = [-1, 1, -2, 2]

    for move in moves:
        new_index = empty_index + move
        if 0 <= new_index < len(state):
            # Create a new state by swapping the empty stone with the rabbit
            new_state = list(state)
            new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
            successors.append(tuple(new_state))

    return successors

def dfs_agent(initial_state, goal_state):
    stack = [(initial_state, [])]
    visited = set()

    while stack:
        state, path = stack.pop()

        if state == goal_state:
            return path + [state]

        if state in visited:
            continue
        visited.add(state)

        successors = get_successors(state)
        for successor in successors:
            if successor not in visited:
                stack.append((successor, path + [state]))

    return None

# Example of using the DFS agent
initial_state = ('E', 'E', 'E', '_', 'W', 'W', 'W')
goal_state = ('W', 'W', 'W', '_', 'E', 'E', 'E')

solution_dfs = dfs_agent(initial_state, goal_state)
print("DFS Solution:")
for step in solution_dfs:
    print(step)
