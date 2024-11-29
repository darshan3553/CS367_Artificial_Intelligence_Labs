import numpy as np

class HopfieldNetwork:
    def __init__(self, size):  # Fixed constructor name
        self.size = size
        self.weights = np.zeros((size, size))

    def train(self, patterns):
        for p in patterns:
            p = np.array(p)
            self.weights += np.outer(p, p) / self.size  # Normalize weights
        np.fill_diagonal(self.weights, 0)  # Zero out diagonal

    def recall(self, input_pattern, steps=10):
        pattern = np.copy(input_pattern)
        for _ in range(steps):
            for i in range(self.size):
                activation = np.dot(self.weights[i], pattern)
                pattern[i] = 1 if activation > 0 else -1
        return pattern

# Example usage
size = 100  # 10x10 grid
patterns = [np.random.choice([-1, 1], size) for _ in range(3)]  # 3 random patterns

hopfield_net = HopfieldNetwork(size)
hopfield_net.train(patterns)

noisy_pattern = np.copy(patterns[0])
noisy_pattern[:10] = -noisy_pattern[:10]  # Introduce noise
recalled_pattern = hopfield_net.recall(noisy_pattern)

print("Recalled Pattern:", recalled_pattern)

# Capacity function
def hopfield_capacity(neurons):
    return int(0.15 * neurons)  # 15% of the number of neurons

# Example usage
neurons = 100  # 10x10 grid
capacity = hopfield_capacity(neurons)
print(f"Capacity of Hopfield Network: {capacity} patterns")

# Test error correction
def test_error_correction(hopfield_net, original_pattern, errors=5):
    noisy_pattern = np.copy(original_pattern)
    noisy_indices = np.random.choice(len(noisy_pattern), errors, replace=False)
    noisy_pattern[noisy_indices] = -noisy_pattern[noisy_indices]  # Flip bits
    recalled_pattern = hopfield_net.recall(noisy_pattern)
    return recalled_pattern

# Example usage
pattern = np.random.choice([-1, 1], 100)  # Random pattern
recalled = test_error_correction(hopfield_net, pattern)
print("Recalled with Error Correction:", recalled)

# Energy function for Hopfield network
def energy_function(board, weights):
    energy = -0.5 * np.sum(np.outer(board, board) * weights)  # Correct energy formula
    return energy

# Example setup for 8-rook problem
board = np.random.choice([-1, 1], 64)  # 8x8 board flattened to 64 elements
weights = np.random.randn(64, 64)  # Random weight matrix for the problem
np.fill_diagonal(weights, 0)  # Ensure diagonal weights are zero
energy = energy_function(board, weights)
print(f"Energy: {energy}")

# TSP Energy Function
def tsp_energy_function(route, distances):
    energy = 0
    for i in range(len(route) - 1):
        energy += distances[route[i], route[i + 1]]  # Add distances sequentially
    energy += distances[route[-1], route[0]]  # Complete the cycle back to start
    return energy

# Example usage for TSP with 10 cities
distances = np.random.randint(1, 100, (10, 10))  # Random distance matrix (symmetric)
distances = (distances + distances.T) // 2  # Symmetrize the matrix
np.fill_diagonal(distances, 0)  # No self-distances
route = np.random.permutation(10)  # Random initial route
energy = tsp_energy_function(route, distances)
print(f"Energy of the TSP route: {energy}")
