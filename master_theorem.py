# master_theorem.py

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


def plot_master_theorem(a: int, b: int, k: int) -> None:
    n = np.linspace(1, 100, 400)
    n_log_b_a = n ** (log(a) / log(b))
    f_n = n ** k

    # Use actual values for a, b, and k in the legend labels
    n_log_b_a_label = f'$n^{{\\log_{{{b}}}({a})}}$' if a != 1 or b != 2 or k != 0 else '$\\log(n)$'
    f_n_label = f'$f(n) = n^{{{k}}}$' if k != 0 else '$f(n) = 1$'  # Special case for k=0

    # Adjust for binary search to directly use log(n)
    if a == 1 and b == 2 and k == 0:
        complexity_label = r'$\Theta(\log n)$'
        time_complexity = np.log(n)
    elif a == 2 and b == 2 and k == 1:  # Specific case for Merge Sort
        complexity_label = r'$\Theta(n \log n)$'
        time_complexity = n * np.log(n)
    elif a in [7, 3] and b == 2:  # Handle Strassen's and Karatsuba's algorithms
        complexity_label = f'$\Theta(n^{{\log_{{{b}}}({a})}})$'  # Directly use log base b of a
        time_complexity = n ** log(a, b)
    else:  # General cases
        if log(a, b).is_integer():
            complexity_label = f'$\Theta(n^{{\log_{{{b}}}({a})}})$'  # Display log base b of a as an integer
            time_complexity = n_log_b_a
        else:
            complexity_label = f'$\Theta(n^{{\log_{{{b}}}({a}):.2f}})$'  # Keep decimal for non-integer log results
            time_complexity = n_log_b_a

    plt.figure(figsize=(10, 6))
    plt.plot(n, n_log_b_a, label=n_log_b_a_label, color='blue')
    plt.plot(n, f_n, label=f_n_label, color='red')
    plt.plot(n, time_complexity, label=complexity_label + " (Time Complexity)", linestyle='--', color='green')

    plt.title('Master Theorem Visualization')
    plt.xlabel('n')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)

    # Place the label for the time complexity curve
    label_y_pos = max(time_complexity) if a != 1 or b != 2 or k != 0 else np.max(np.log(n))
    plt.text(n[-1] * 0.9, label_y_pos, complexity_label, fontsize=12, verticalalignment='bottom')

    plt.show()


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