# master_theorem.py

from math import log
import matplotlib.pyplot as plt
import numpy as np

def evaluate_master_theorem(a, b, k):
    if not all(isinstance(param, int) for param in [a, b, k]):
        raise ValueError("All parameters (a, b, k) must be integers.")
    if a <= 0:
        raise ValueError("Parameter 'a' must be greater than 0.")
    if b <= 1:
        raise ValueError("Parameter 'b' must be greater than 1.")
    if k < 0:
        raise ValueError("Parameter 'k' must be non-negative.")
    
    log_b_a = log(a, b)
    
    if log_b_a > k:
        complexity = f"Θ(n^{log_b_a:.2f})"
        case = "Case 1"
    elif log_b_a == k:
        complexity = "Θ(n^k log n)"
        case = "Case 2"
    else:
        complexity = f"Θ(n^{k})"
        case = "Case 3"
    return complexity, case


def plot_master_theorem(a, b, k):
    n = np.linspace(1, 100, 400)  # Generate an array of n values from 1 to 100
    n_log_b_a = n ** (np.log(a) / np.log(b))  # Calculate n^(log_b(a))
    f_n = n ** k  # Calculate f(n) = n^k
    
    # Determine the complexity for labeling and plotting
    log_b_a = np.log(a) / np.log(b)
    if log_b_a > k:
        complexity = r'$\Theta(n^{\log_b(a)})$'
        complexity_function = n_log_b_a
    elif log_b_a == k:
        complexity = r'$\Theta(n^k \log n)$'
        complexity_function = n ** k * np.log(n)
    else:
        complexity = r'$\Theta(n^k)$'
        complexity_function = f_n
    
    plt.figure(figsize=(10, 6))
    
    # Plot n^(log_b(a))
    plt.plot(n, n_log_b_a, label=r'$n^{\log_b(a)}$', color='blue')
    
    # Plot f(n) = n^k
    plt.plot(n, f_n, label=r'$f(n) = n^k$', color='red')
    
    # Plot the time complexity function
    plt.plot(n, complexity_function, label=complexity + ' (Time Complexity)', color='green', linestyle='--')
    
    plt.xlabel('n')
    plt.ylabel('Value')
    plt.title('Master Theorem Visualization')
    plt.legend()
    plt.grid(True)

    plt.show()


def main():
    # Prompt user for input
    print("Enter the values for evaluating the Master Theorem:")
    a = float(input("a (number of subproblems): "))
    b = float(input("b (factor by which the problem size is reduced): "))
    k = float(input("k (exponent in the work done outside the recursive calls): "))

    # Evaluate and display the result
    complexity, case = evaluate_master_theorem(a, b, k)
    print(f"\nRecurrence Relation: T(n) = {a}T(n/{b}) + n^{k}")
    print(f"Complexity: {complexity} ({case})")

    # Plot the visualization
    plot_master_theorem(a, b, k)  


if __name__ == '__main__':
    main()