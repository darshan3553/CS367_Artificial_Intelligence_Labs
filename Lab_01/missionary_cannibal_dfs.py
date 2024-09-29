from collections import deque

class State:
    def __init__(self, m_left, c_left, boat, m_right, c_right, parent=None):
        self.m_left = m_left
        self.c_left = c_left
        self.boat = boat  # 1 means boat on the left, 0 means boat on the right
        self.m_right = m_right
        self.c_right = c_right
        self.parent = parent  # To backtrack and print the solution path

    def is_valid(self):
        """Check if the current state is valid."""
        if self.m_left >= 0 and self.m_right >= 0 \
           and self.c_left >= 0 and self.c_right >= 0 \
           and (self.m_left == 0 or self.m_left >= self.c_left) \
           and (self.m_right == 0 or self.m_right >= self.c_right):
            return True
        return False

    def is_goal(self):
        """Check if we have reached the goal."""
        return self.m_left == 0 and self.c_left == 0

    def __eq__(self, other):
        return self.m_left == other.m_left \
               and self.c_left == other.c_left \
               and self.boat == other.boat \
               and self.m_right == other.m_right \
               and self.c_right == other.c_right

    def __hash__(self):
        return hash((self.m_left, self.c_left, self.boat, self.m_right, self.c_right))

    def get_successors(self):
        """Generate all valid successor states."""
        successors = []
        if self.boat == 1:  # Boat on the left side
            moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]  # All possible moves: (M, C)
            for m, c in moves:
                new_state = State(self.m_left - m, self.c_left - c, 0,
                                  self.m_right + m, self.c_right + c, self)
                if new_state.is_valid():
                    successors.append(new_state)
        else:  # Boat on the right side
            moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
            for m, c in moves:
                new_state = State(self.m_left + m, self.c_left + c, 1,
                                  self.m_right - m, self.c_right - c, self)
                if new_state.is_valid():
                    successors.append(new_state)
        return successors

def print_solution(solution):
    """Print the solution path from start to goal."""
    path = []
    while solution:
        path.append(solution)
        solution = solution.parent

    # Print the solution from start to goal
    for state in path[::-1]:
        m_left = state.m_left
        c_left = state.c_left
        m_right = state.m_right
        c_right = state.c_right
        boat = "left" if state.boat == 1 else "right"
        
        # Calculate how many are in the boat (total initial is 3)
        missionaries_in_boat = 3 - (m_left + m_right)
        cannibals_in_boat = 3 - (c_left + c_right)
        
        print(f"Left -> Missionaries: {m_left}, Cannibals: {c_left}")
        print(f"Right -> Missionaries: {m_right}, Cannibals: {c_right}")
        print("-" * 40)

def dfs(start_state):
    """Depth-First Search algorithm."""
    stack = [start_state]
    visited = set()
    visited.add(start_state)
    number_of_visited_states = 0

    while stack:
        state = stack.pop()
        number_of_visited_states += 1

        if state.is_goal():
            print("Solution found with DFS!")
            print_solution(state)
            print(f"Number of visited states: {number_of_visited_states}")
            return True

        for successor in state.get_successors():
            if successor not in visited:
                stack.append(successor)
                visited.add(successor)

    print("No solution found with DFS.")
    return False

# Initial state: 3 missionaries and 3 cannibals on the left side, boat on the left
start_state = State(3, 3, 1, 0, 0)

# Solve using DFS
print("DFS Solution:")
dfs(start_state)
