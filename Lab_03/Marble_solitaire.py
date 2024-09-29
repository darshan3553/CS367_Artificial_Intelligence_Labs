import heapq
import time

# Directions for the movement in the game (up, down, left, right)
MOVES = [(2, 0), (-2, 0), (0, 2), (0, -2)]

# Helper function to clone the board
def clone_board(board):
    return [row[:] for row in board]

# Helper function to check if a move is valid
def is_valid_move(board, x, y, dx, dy):
    if 0 <= x + dx < len(board) and 0 <= y + dy < len(board[0]):
        mid_x, mid_y = x + dx // 2, y + dy // 2
        return board[x][y] == 1 and board[x + dx][y + dy] == 0 and board[mid_x][mid_y] == 1
    return False

# Apply the move (jump over a marble)
def apply_move(board, x, y, dx, dy):
    new_board = clone_board(board)
    mid_x, mid_y = x + dx // 2, y + dy // 2
    new_board[x][y] = 0
    new_board[mid_x][mid_y] = 0
    new_board[x + dx][y + dy] = 1
    return new_board

# Heuristic 1: Number of remaining marbles
def heuristic_num_marbles(board):
    return sum(sum(1 for cell in row if cell == 1) for row in board)

# Heuristic 2: Total Manhattan distance to the center
def heuristic_manhattan(board):
    center = (3, 3)
    total_distance = 0
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 1:
                total_distance += abs(center[0] - x) + abs(center[1] - y)
    return total_distance

# Combined heuristic: Number of marbles + Manhattan distance
def combined_heuristic(board):
    return heuristic_num_marbles(board) + heuristic_manhattan(board)

# Priority queue-based search algorithm for Best-First Search (ignoring path cost)
def best_first_search(board, heuristic):
    pq = []
    initial_cost = heuristic(board)
    heapq.heappush(pq, (initial_cost, board, []))  # (heuristic cost, board, path)
    
    visited = set()
    visited.add(tuple(map(tuple, board)))
    nodes_expanded = 0

    while pq:
        nodes_expanded += 1
        _, current_board, path = heapq.heappop(pq)

        # Check if solution (only one marble in the center)
        if heuristic_num_marbles(current_board) == 1 and current_board[3][3] == 1:
            return path, nodes_expanded
        
        for x in range(len(current_board)):
            for y in range(len(current_board[0])):
                if current_board[x][y] == 1:
                    for dx, dy in MOVES:
                        if is_valid_move(current_board, x, y, dx, dy):
                            new_board = apply_move(current_board, x, y, dx, dy)
                            new_board_tuple = tuple(map(tuple, new_board))
                            if new_board_tuple not in visited:
                                visited.add(new_board_tuple)
                                heapq.heappush(pq, (heuristic(new_board), new_board, path + [(x, y, dx, dy)]))

    return None, nodes_expanded

# Priority queue-based search algorithm for A* (considering both heuristic and path cost)
def a_star_search(board, heuristic):
    pq = []
    initial_cost = heuristic(board) + 0  # Start path cost is zero
    heapq.heappush(pq, (initial_cost, board, 0, []))  # (heuristic + path cost, board, path cost, path)
    
    visited = set()
    visited.add(tuple(map(tuple, board)))
    nodes_expanded = 0

    while pq:
        nodes_expanded += 1
        _, current_board, current_cost, path = heapq.heappop(pq)

        # Check if solution (only one marble in the center)
        if heuristic_num_marbles(current_board) == 1 and current_board[3][3] == 1:
            return path, current_cost, nodes_expanded
        
        for x in range(len(current_board)):
            for y in range(len(current_board[0])):
                if current_board[x][y] == 1:
                    for dx, dy in MOVES:
                        if is_valid_move(current_board, x, y, dx, dy):
                            new_board = apply_move(current_board, x, y, dx, dy)
                            new_board_tuple = tuple(map(tuple, new_board))
                            if new_board_tuple not in visited:
                                visited.add(new_board_tuple)
                                new_cost = current_cost + 1
                                heapq.heappush(pq, (new_cost + heuristic(new_board), new_board, new_cost, path + [(x, y, dx, dy)]))

    return None, None, nodes_expanded

# Board initialization
def initialize_board():
    board = [[-1, -1,  1,  1,  1, -1, -1],
             [-1, -1,  1,  1,  1, -1, -1],
             [ 1,  1,  1,  1,  1,  1,  1],
             [ 1,  1,  1,  0,  1,  1,  1],
             [ 1,  1,  1,  1,  1,  1,  1],
             [-1, -1,  1,  1,  1, -1, -1],
             [-1, -1,  1,  1,  1, -1, -1]]
    return board

# Main comparison of algorithms
def compare_algorithms():
    board = initialize_board()
    
    # Best-First Search with Number of Marbles Heuristic
    start_time = time.time()
    print("Solving with Best-First Search (Number of Marbles Heuristic)")
    path, nodes_expanded = best_first_search(board, heuristic_num_marbles)
    time_taken = time.time() - start_time
    if path is not None:
        print(f"Solution found with Best-First Search (Number of Marbles Heuristic). Path: {path}")
    else:
        print("No solution found with Best-First Search (Number of Marbles Heuristic).")
    print(f"Time Taken: {time_taken:.6f} seconds\n")

    # Best-First Search with Manhattan Distance Heuristic
    start_time = time.time()
    print("Solving with Best-First Search (Manhattan Distance Heuristic)")
    path, nodes_expanded = best_first_search(board, heuristic_manhattan)
    time_taken = time.time() - start_time
    if path is not None:
        print(f"Solution found with Best-First Search (Manhattan Distance Heuristic). Path: {path}")
    else:
        print("No solution found with Best-First Search (Manhattan Distance Heuristic).")
    print(f"Time Taken: {time_taken:.6f} seconds\n")

    # A* Search with Combined Heuristic
    start_time = time.time()
    print("Solving with A* (Combined Heuristic: Number of Marbles + Manhattan Distance)")
    path, cost, nodes_expanded = a_star_search(board, combined_heuristic)
    time_taken = time.time() - start_time
    if path is not None:
        print(f"Solution found with A* (Combined Heuristic) with path cost {cost}. Path: {path}")
    else:
        print("No solution found with A* (Combined Heuristic).")
    print(f"Time Taken: {time_taken:.6f} seconds")

# Run the comparison
compare_algorithms()
