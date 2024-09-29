import random

def generate_k_sat_problem(k, m, n):
    choices = []
    for i in range(n):
        choices.append(chr(ord('a') + i)) 

    ans = ""
    for _ in range(m):  
        ans += "("
        selected_vars = random.sample(choices, k)  
        for j in range(k):
            sign = random.choice([-1, 1])  
            if sign == 1:
                ans += selected_vars[j]  
            else:
                ans += f"-{selected_vars[j]}"  
            if j < k - 1:
                ans += " ∨ "  
        ans += ")"
        if _ < m - 1:
            ans += " ∧ " 

    print(ans)

def main():
    k = int(input("Enter the length of clause k: "))
    m = int(input("Enter the number of clauses m: "))
    n = int(input("Enter the number of variables n (max 26): "))
    p = int(input("Enter the number of problems to be generated: "))
    
    for i in range(p):
        print(f"\nProblem {i + 1}:")
        generate_k_sat_problem(k, m, n)
        
if __name__== "__main__":
    # Your code here
    main()