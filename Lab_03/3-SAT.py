import random

def generate_3sat_problem(n, m):
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < 3:
            variable = random.randint(1, n)
            if random.random() < 0.5:  # Randomly negate the variable
                variable = -variable
            clause.add(variable)
        clauses.append(clause)
    return clauses

def evaluate_solution(solution, clauses):
    return all(any((var > 0 and solution[var - 1]) or (var < 0 and not solution[-var - 1]) for var in clause) for clause in clauses)

def count_satisfied_clauses(solution, clauses):
    return sum(1 for clause in clauses if any((var > 0 and solution[var - 1]) or (var < 0 and not solution[-var - 1]) for var in clause))

def hill_climbing(clauses, n):
    current_solution = [random.choice([True, False]) for _ in range(n)]
    while True:
        if evaluate_solution(current_solution, clauses):
            return current_solution
        
        neighbors = []
        for i in range(n):
            neighbor = current_solution[:]
            neighbor[i] = not neighbor[i]
            neighbors.append(neighbor)

        # Select the best neighbor
        best_neighbor = max(neighbors, key=lambda s: count_satisfied_clauses(s, clauses))
        if count_satisfied_clauses(best_neighbor, clauses) > count_satisfied_clauses(current_solution, clauses):
            current_solution = best_neighbor
        else:
            break
    return None  # No solution found

def beam_search(clauses, n, beam_width):
    current_solutions = [[random.choice([True, False]) for _ in range(n)] for _ in range(beam_width)]
    
    while True:
        new_solutions = []
        for solution in current_solutions:
            if evaluate_solution(solution, clauses):
                return solution
            
            for i in range(n):
                neighbor = solution[:]
                neighbor[i] = not neighbor[i]
                new_solutions.append(neighbor)

        # Keep the best solutions based on the number of satisfied clauses
        current_solutions = sorted(new_solutions, key=lambda s: count_satisfied_clauses(s, clauses), reverse=True)[:beam_width]
        
        if not current_solutions:
            break  # No solutions found
    return None

def variable_neighborhood_descent(clauses, n):
    def neighborhood1(solution):
        return [solution[:i] + [not solution[i]] + solution[i + 1:] for i in range(n)]
    
    def neighborhood2(solution):
        return [solution[:i] + [not solution[i]] + solution[:j] + solution[j + 1:] for i in range(n) for j in range(i + 1, n)]
    
    def neighborhood3(solution):
        return [solution[:i] + [not solution[i]] + solution for i in range(n)]
    
    neighborhoods = [neighborhood1, neighborhood2, neighborhood3]
    current_solution = [random.choice([True, False]) for _ in range(n)]

    while True:
        if evaluate_solution(current_solution, clauses):
            return current_solution
        
        best_solution = current_solution
        for neighborhood in neighborhoods:
            for neighbor in neighborhood(current_solution):
                if evaluate_solution(neighbor, clauses):
                    return neighbor
                if count_satisfied_clauses(neighbor, clauses) > count_satisfied_clauses(best_solution, clauses):
                    best_solution = neighbor
        
        if best_solution == current_solution:
            break
        current_solution = best_solution

    return None  # No solution found

def compare_performance():
    n = int(input("Enter the number of variables: "))
    m = int(input("Enter the number of clauses: "))
    beam_width = int(input("Enter the beam width: "))
    
    clauses = generate_3sat_problem(n, m)
    
    print("Variables are:", [f'v{i+1}' for i in range(n)])
    
    # Print generated expression
    expression = ' & '.join(f'({"|".join(f"(!v{abs(var)})" if var < 0 else f"v{var}" for var in clause)})' for clause in clauses)
    print("Expression Generated is:", expression)
    
    hill_climbing_solution = hill_climbing(clauses, n)
    print("Hill Climbing solution:", [int(x) for x in hill_climbing_solution], ", Satisfied clauses:", count_satisfied_clauses(hill_climbing_solution, clauses), "/", m)

    beam_search_solution = beam_search(clauses, n, beam_width)
    print("Beam Search solution:", [int(x) for x in beam_search_solution], ", Satisfied clauses:", count_satisfied_clauses(beam_search_solution, clauses), "/", m)

    variable_neighborhood_solution = variable_neighborhood_descent(clauses, n)
    print("Variable Neighborhood Descent solution:", [int(x) for x in variable_neighborhood_solution], ", Satisfied clauses:", count_satisfied_clauses(variable_neighborhood_solution, clauses), "/", m)

# Run the performance comparison with user input
compare_performance()
