# master_theorem.py

import os
from django.conf import settings
from math import log
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple

def evaluate_master_theorem(a: int, b: int, k: int) -> Tuple[str, str]:
    # Ensure all parameters are integers and meet specific constraints
    if not all(isinstance(param, int) for param in [a, b, k]):
        raise ValueError("All parameters (a, b, k) must be integers.")
    if a <= 0:
        raise ValueError("Parameter 'a' must be greater than 0.")
    if b <= 1:  # Identify b = 1 as an error case.
        raise ValueError("Parameter 'b' must be greater than 1 to ensure the problem size is reduced.")
    if k < 0:
        raise ValueError("Parameter 'k' must be non-negative.")

    log_b_a = log(a, b)
    
    if log_b_a > k:
        complexity = f"Θ(n^{log_b_a})" if isinstance(log_b_a, int) else f"Θ(n^{log_b_a:.2f})"
        case = "Case 1"
    elif log_b_a == k:
        complexity = "Θ(n^k log n)"
        case = "Case 2"
    else:
        complexity = f"Θ(n^{k})"
        case = "Case 3"
    
    return complexity, case


def plot_master_theorem(a: int, b: int, k: int, filename: str) -> str:
    n = np.linspace(1, 100, 400)
    log_b_a = log(a, b)

    # Simplify the label for f(n)
    f_n_label = 'f(n)'

    # Determine the case based on a, b, and k
    if a == 1 and b == 2 and k == 0:
        # Special case for Binary Search
        complexity_label = r'$\Theta(\log n)$'
        time_complexity = np.log(n)
    elif a == 2 and b == 2 and k == 1:
        # Special case for Merge Sort
        complexity_label = r'$\Theta(n \log n)$'
        time_complexity = n * np.log(n)
    else:
        if log_b_a > k:
            # Case 1: T(n) = Θ(n^log_b(a))
            complexity_label = f'$\\Theta(n^{{\\log_{{{b}}}({a})}})$' if not log_b_a.is_integer() else f'$\\Theta(n^{{{int(log_b_a)}}})$'
            time_complexity = n ** log_b_a
        elif log_b_a == k:
            # Adjust formatting for n^1 log(n) to n log(n)
            complexity_label = r'$\Theta(n \log n)$' if k == 1 else r'$\Theta(n^' + str(k) + r' \log n)$'
            time_complexity = n ** k * np.log(n)
        else:
            # Case 3: T(n) = Θ(n^k), with special handling to omit n^0
            complexity_label = r'$\Theta(1)$' if k == 0 else f'$\\Theta(n^{{{k}}})$'
            time_complexity = np.ones_like(n) if k == 0 else n ** k

    plt.figure(figsize=(10, 6))
    plt.plot(n, n ** log_b_a, label='$n^{\\log_b a}$', color='blue')
    plt.plot(n, n ** k, label=f'{f_n_label}', linestyle='--', color='red')
    plt.plot(n, time_complexity, label='T(n) (Time Complexity)', linestyle='-', color='green')

    plt.title('Master Theorem Visualization')
    plt.xlabel('n')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)

    # Add annotation for time complexity
    plt.text(0.5, 0.95, 'T(n) = ' + complexity_label, horizontalalignment='center',
             verticalalignment='center', transform=plt.gca().transAxes, fontsize=12, color='purple', bbox=dict(facecolor='white', alpha=0.5))

    plt.show()
    plot_path = os.path.join(settings.BASE_DIR, 'static', 'plots', filename)
    plt.savefig(plot_path)

    return os.path.join('static', 'plots', filename)


def main() -> None:
    print("Enter the values for evaluating the Master Theorem:")
    
    # Read inputs as floats first
    a_input = float(input("a (number of subproblems): "))
    b_input = float(input("b (factor by which the problem size is reduced): "))
    k_input = float(input("k (exponent in the work done outside the recursive calls): "))

    # Validate inputs to ensure they can be converted to integers without losing precision
    if not (a_input.is_integer() and b_input.is_integer() and k_input.is_integer()):
        print("Error: All parameters must be integers.")
        return  # Exit the function early or handle the error as appropriate

    # Convert inputs to integers
    a = int(a_input)
    b = int(b_input)
    k = int(k_input)

    # Proceed with the evaluation and plotting
    complexity, case = evaluate_master_theorem(a, b, k)
    print(f"\nRecurrence Relation: T(n) = {a}T(n/{b}) + n^{k}")
    print(f"Complexity: {complexity} ({case})")

    plot_master_theorem(a, b, k)


if __name__ == '__main__':
    main()