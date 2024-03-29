# master_theorem.py

import os
from django.conf import settings
from math import log
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple

CASE_1 = f"Case 1: Θ(n<sup>log<sub>b</sub>(a)</sup>)"
CASE_2 = f"Case 2: Θ(n<sup>k</sup> log n)"
CASE_3 = f"Case 3: Θ(n<sup>k</sup>)"

def check_regularity_condition(a: int, b: int, k: int) -> bool:
    # check if a/b^k < 1
    return a / b ** k < 1

def evaluate_master_theorem(a: int, b: int, k: int) -> Tuple[str, str, str, bool]:
    if a<= 0:
        raise ValueError("Parameter 'a' must be greater than 0.")
    if b <= 1:
        raise ValueError("Parameter 'b' must be greater than 1 to ensure the problem size is reduced.")
    
    log_b_a = log(a, b)
    log_b_a_is_integer = log_b_a.is_integer()
    
    # Define the complexity and cases with dynamic formatting
    if log_b_a > k:
        complexity = f"Θ(n<sup>{int(log_b_a) if log_b_a_is_integer else f'log<sub>{b}</sub>({a})'}</sup>)"
        case = CASE_1
    elif log_b_a == k:
        if k == 0:
            complexity = "Θ(log n)"
        elif k == 1:
            complexity = "Θ(n log n)"
        else:
            complexity = f"Θ(n<sup>{k}</sup> log n)"
        case = CASE_2
    else: # log_b_a < k
        if k == 0:
            complexity = "Θ(1)" # Omitting n^0 for clarity
            case = CASE_3
        elif k == 1:
            complexity = "Θ(n)" # Displaying n without exponent
            case = CASE_3
        else:
            complexity = f"Θ(n<sup>{k}</sup>)" # Using exponent k
            case = CASE_3
    
    regularity_condition_met = False
    if log_b_a < k:
        regularity_condition_met = check_regularity_condition(a, b, k)
        if not regularity_condition_met:
            case += " (Regularity Condition Not Met)"
    
    # Format recurrence relation according to the value of k
    if k > 0:
        recurrence_relation = f"T(n) = {a}T(n/{b}) + f(n<sup>{k}</sup>)"
    else: # k == 0, implies f(n^0) which is f(1), so typically not shown
        recurrence_relation = f"T(n) = {a}T(n/{b}) + f(1)"
    
    return complexity, case, recurrence_relation, regularity_condition_met




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
    plot_path = os.path.join(settings.MEDIA_ROOT, 'plots', filename)
    plt.savefig(plot_path)

    return os.path.join('plots', filename)

def calculate_plot_data(a: int, b: int, k: int) -> dict:
    n = np.linspace(1, 100, 400)
    log_b_a = np.log(a) / np.log(b)

    # Element-wise exponentiation for n^log_b(a)
    n_log_b_a = n ** log_b_a

    # Adjust f(n) based on the case
    if log_b_a > k:
        f_n = (n ** k).tolist()  # Case 1
    elif log_b_a == k:
        # Since k = log_b(a) for Case 2, adjust f(n) to reflect n^k for comparison purposes
        f_n = (n ** k).tolist()  # f(n) = n^k for visual comparison
    else:
        f_n = (np.ones_like(n) if k == 0 else n ** k).tolist()  # Case 3

    # Adjust time complexity calculation to match the Master Theorem's conclusions accurately
    if log_b_a > k:
        time_complexity = n_log_b_a.tolist()  # Case 1
    elif log_b_a == k:
        # For Case 2, adjust time complexity to reflect n^log_b(a) * log n
        time_complexity = (n ** log_b_a * np.log(n)).tolist()
    else:
        time_complexity = f_n  # Case 3

    return {
        'n': n.tolist(),
        'n_log_b_a': n_log_b_a.tolist(),
        'f_n': f_n,
        'time_complexity': time_complexity,
    }

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
    complexity, case, recurrence_relation, _ = evaluate_master_theorem(a, b, k)
    print(f"\nRecurrence Relation: {recurrence_relation}")
    print(f"Complexity: {complexity} ({case})")

    plot_master_theorem(a, b, k, 'filename.png')


if __name__ == '__main__':
    main()