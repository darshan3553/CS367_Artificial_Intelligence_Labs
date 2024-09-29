from collections import deque
import tracemalloc
import time  # Add this import for tracking execution time


goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

def get_successors(node):
    """Generate all valid successor states from the current state."""
    successors = []
    state = node.state 
    blank_index = state.index(0)
    row, col = divmod(blank_index, 3)
    
    # Define possible moves (up, down, left, right)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for move in moves:
        new_row, new_col = row + move[0], col + move[1]
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank_index = new_row * 3 + new_col
            new_state = state[:]
            new_state[blank_index], new_state[new_blank_index] = new_state[new_blank_index], new_state[blank_index]
            successors.append(Node(new_state, node))
    
    return successors

def is_solvable(state):
    """Check if the 8-puzzle is solvable by counting inversions."""
    inversions = 0
    state = [tile for tile in state if tile != 0]  # Exclude the blank tile
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] > state[j]:
                inversions += 1
    return inversions % 2 == 0

def dfs(start_state, goal_state):
    """Perform Depth-First Search (DFS) to find the shortest solution path."""
    start_node = Node(start_state)
    stack = [start_node]
    visited = set()
    nodes_explored = 0

    while stack:
        node = stack.pop()
        if tuple(node.state) in visited:
            continue
        visited.add(tuple(node.state))
        nodes_explored += 1

        if node.state == goal_state:
            # Backtrack to construct the solution path
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            print(f"Solution found! Total nodes explored: {nodes_explored}")
            return path[::-1]

        for successor in get_successors(node):
            if tuple(successor.state) not in visited:
                stack.append(successor)

    print(f"No solution found. Total nodes explored: {nodes_explored}")
    return None

def print_solution(solution):
    """Print the solution steps in a readable format."""
    for step_num, step in enumerate(solution, start=1):
        print(f"Step {step_num}:")
        for i in range(0, 9, 3):
            print(step[i:i+3])
        print()

# Input validation function
def get_valid_input():
    while True:
        try:
            start_state = [int(x) for x in input("Enter the start state of the puzzle (9 space-separated numbers from 0-8): ").split()]
            if len(start_state) != 9 or set(start_state) != set(range(9)):
                raise ValueError
            return start_state
        except ValueError:
            print("Invalid input. Please enter exactly 9 numbers between 0 and 8, with no duplicates.")

# Main execution with memory tracking
if __name__ == "__main__":
    start_state = get_valid_input()

    if is_solvable(start_state):
        tracemalloc.start()
        start_time = time.time()
        
        solution = dfs(start_state, goal_state)
        
        end_time = time.time()
        memory_peak = tracemalloc.get_traced_memory()[1] / 1024  # Convert to KB
        tracemalloc.stop()
        
        if solution:
            print("Solution path:")
            print_solution(solution)
        else:
            print("No solution found.")
    else:
        print("The given start state is not solvable.")
