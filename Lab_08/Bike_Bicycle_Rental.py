import numpy as np
import scipy.stats as stats

# Constants
MAX_BIKES_PER_LOCATION = 20  # Maximum bikes at each station
MAX_TRANSFER_LIMIT = 5       # Maximum bikes transferable between locations
DISCOUNT_RATE = 0.9          # Discount factor for future rewards
RENTAL_INCOME = 10           # Earnings per bike rented
TRANSFER_COST = 2            # Cost per bike moved (first move may be free)
OVER_CAPACITY_FINE = 4       # Cost for parking more than 10 bikes

# Average Poisson-distributed bike requests and returns for the locations
AVG_REQUESTS_LOC_1 = 3
AVG_REQUESTS_LOC_2 = 4
AVG_RETURNS_LOC_1 = 3
AVG_RETURNS_LOC_2 = 2

# Define the state and action spaces
states = [(i, j) for i in range(MAX_BIKES_PER_LOCATION + 1) for j in range(MAX_BIKES_PER_LOCATION + 1)]
actions = list(range(-MAX_TRANSFER_LIMIT, MAX_TRANSFER_LIMIT + 1))

# Function to compute Poisson probabilities
def poisson_distribution(mean):
    return stats.poisson.pmf(np.arange(MAX_BIKES_PER_LOCATION + 1), mean)

# Function to compute the reward based on the state and action
def calculate_reward(state, transfer):
    bikes_loc_1, bikes_loc_2 = state
    
    # Moving bikes incurs a cost (except for specific conditions, e.g., a free move)
    transfer_cost = 0 if transfer == -1 else TRANSFER_COST * abs(transfer)
    
    # Calculate rentals and corresponding income
    rentals_loc_1 = min(AVG_REQUESTS_LOC_1, bikes_loc_1)
    rentals_loc_2 = min(AVG_REQUESTS_LOC_2, bikes_loc_2)
    total_income = RENTAL_INCOME * (rentals_loc_1 + rentals_loc_2)
    
    # Parking penalty for exceeding capacity at either location
    parking_penalty = 0
    if bikes_loc_1 + transfer > 10:
        parking_penalty += OVER_CAPACITY_FINE
    if bikes_loc_2 - transfer > 10:
        parking_penalty += OVER_CAPACITY_FINE
    
    return total_income - transfer_cost - parking_penalty

# Function to compute the next state based on current state and action
def compute_next_state(state, transfer):
    bikes_loc_1, bikes_loc_2 = state
    
    # Update bike counts after rentals and returns
    updated_loc_1 = min(MAX_BIKES_PER_LOCATION, max(0, bikes_loc_1 - min(bikes_loc_1, AVG_REQUESTS_LOC_1) + AVG_RETURNS_LOC_1 - transfer))
    updated_loc_2 = min(MAX_BIKES_PER_LOCATION, max(0, bikes_loc_2 - min(bikes_loc_2, AVG_REQUESTS_LOC_2) + AVG_RETURNS_LOC_2 + transfer))
    
    return updated_loc_1, updated_loc_2

# Policy iteration function to optimize the policy
def perform_policy_iteration():
    # Initialize the value function and policy
    value_function = np.zeros((MAX_BIKES_PER_LOCATION + 1, MAX_BIKES_PER_LOCATION + 1))
    policy = np.zeros((MAX_BIKES_PER_LOCATION + 1, MAX_BIKES_PER_LOCATION + 1), dtype=int)
    
    # Random initial policy assignment
    for state in states:
        policy[state[0], state[1]] = np.random.choice(actions)
    
    # Iterative process
    while True:
        # Policy evaluation: Update value function for the current policy
        updated_values = np.copy(value_function)
        for state in states:
            chosen_action = policy[state[0], state[1]]
            immediate_reward = calculate_reward(state, chosen_action)
            next_s = compute_next_state(state, chosen_action)
            updated_values[state[0], state[1]] = immediate_reward + DISCOUNT_RATE * value_function[next_s[0], next_s[1]]
        
        # Policy improvement: Update the policy based on the new value function
        policy_stable = True
        for state in states:
            previous_action = policy[state[0], state[1]]
            action_rewards = []
            
            # Compute value for each possible action
            for action in actions:
                reward_value = calculate_reward(state, action)
                next_s = compute_next_state(state, action)
                action_rewards.append(reward_value + DISCOUNT_RATE * value_function[next_s[0], next_s[1]])
            
            # Choose the best action
            optimal_action = actions[np.argmax(action_rewards)]
            policy[state[0], state[1]] = optimal_action
            
            # Check if policy has changed
            if previous_action != optimal_action:
                policy_stable = False
        
        # If no changes in policy, exit the loop
        if policy_stable:
            break
        
        # Update the value function
        value_function = np.copy(updated_values)
    
    return value_function, policy

# Execute the policy iteration algorithm
optimal_values, optimal_policy = perform_policy_iteration()

# Display the results
print("Optimal Value Function:")
print(optimal_values)

print("\nOptimal Policy:")
print(optimal_policy)
