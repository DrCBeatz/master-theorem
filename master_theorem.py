# master_theorem.py

from sympy import log, oo, limit, solve, Symbol, simplify

def check_regularity_condition(a, b, f_n, n_symbol):
    """
    Checks the regularity condition for Case 3.
    """
    k = Symbol('k', real=True)  # Symbol for the constant k in the regularity condition
    n_b = simplify(n_symbol / b)  # Simplify n/b for substitution
    lhs = a * f_n.subs(n_symbol, n_b)  # Calculate af(n/b)
    rhs = k * f_n  # Calculate kf(n)

    # Solve for k to check if there exists a k < 1 that satisfies the inequality
    k_solution = solve(lhs - rhs, k)

    if k_solution:
        # Check if any solution for k satisfies k < 1
        for sol in k_solution:
            if sol < 1:
                return True  # Regularity condition is satisfied
    return False  # Regularity condition is not satisfied or could not be verified

def master_theorem(a, b, f_n, n_symbol):
    """
    Evaluate the Master Theorem for a given recurrence relation.
    
    Parameters:
    - a: The number of subproblems into which the problem is divided.
    - b: The factor by which the subproblem size is reduced.
    - f_n: The function f(n) as a SymPy expression.
    - n_symbol: The symbol used for n in f_n.
    
    Returns:
    - The asymptotic behavior of T(n).
    """
    # Calculate n^(log_b(a))
    n_log_b_a = n_symbol ** log(a, b)
    
    # Use limits to compare the growth rates of f(n) and n^(log_b(a))
    limit_comparison = limit(f_n / n_log_b_a, n_symbol, oo)
    
    # Specifically handle constant or slower-growing f(n) for Case 1
    if simplify(f_n).is_constant():
        # If f(n) is constant, it typically leads to a logarithmic complexity
        return "Case 1: T(n) = Theta(log n)"
    elif limit_comparison == 0:
        # For non-constant f(n) that grows slower than n^(log_b(a))
        return f"Case 1: T(n) = Theta(n^{log(a, b)})"
    elif limit_comparison == oo and not check_regularity_condition(a, b, f_n, n_symbol):
        return "Further analysis required, regularity condition not satisfied."
    elif limit_comparison == oo:
        # Case 3 with regularity condition satisfied
        return f"Case 3: T(n) = Theta({f_n})"
    else:
        # Case 2 where f(n) grows at a rate comparable to n^(log_b(a))
        return f"Case 2: T(n) = Theta(n^{log(a, b)} log(n))"

