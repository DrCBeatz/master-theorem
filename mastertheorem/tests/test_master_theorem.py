# mastertheorem/tests/test_master_theorem.py

import pytest
from mastertheorem.master_theorem import evaluate_master_theorem, calculate_plot_data
import numpy as np

@pytest.mark.parametrize("a,b,k,expected_start,expected_case,description", [
    # Valid test cases, ensuring all parameters are integers
    (4, 2, 1, "Θ(n^", "Case 1", "Generic algorithm - Case 1 (faster growth of recursive part)"),
    (4, 2, 2, "Θ(n^k log n)", "Case 2", "Generic algorithm - Case 2 (balanced growth)"),
    (4, 2, 3, "Θ(n^", "Case 3", "Generic algorithm - Case 3 (faster growth of non-recursive part)"),
    (2, 2, 1, "Θ(n^k log n)", "Case 2", "Merge Sort"),
    (7, 2, 2, "Θ(n^", "Case 1", "Strassen's Matrix Multiplication"),
    (1, 2, 0, "Θ(n^k log n)", "Case 2", "Binary Search"),
    (3, 2, 1, "Θ(n^", "Case 1", "Karatsuba's Algorithm"),
    # Tests for handling invalid input gracefully
    (0, 2, 1, "Error", "Error", "Zero subproblems - expected error"),
    (2, 1, 1, "Error", "Error", "Division by 1 - expected error"),
    (-1, 2, 1, "Error", "Error", "Negative subproblems - expected error"),
])
def test_master_theorem_cases(a: int, b: int, k: int, expected_start: str, expected_case: str, description: str) -> None:
    if expected_case == "Error":
        with pytest.raises(ValueError):
            evaluate_master_theorem(a, b, k)
    else:
        complexity, case = evaluate_master_theorem(a, b, k)
        assert complexity.startswith(expected_start) and case == expected_case, f"Failed for {description}: {complexity}, {case}"

@pytest.mark.parametrize("a,b,k,expected_keys", [
    (1, 2, 0, ['n', 'n_log_b_a', 'f_n', 'time_complexity']),
    (2, 2, 1, ['n', 'n_log_b_a', 'f_n', 'time_complexity']),
    (7, 2, 2, ['n', 'n_log_b_a', 'f_n', 'time_complexity']),
    (3, 2, 1, ['n', 'n_log_b_a', 'f_n', 'time_complexity']),
    (4, 2, 1, ['n', 'n_log_b_a', 'f_n', 'time_complexity']),
    (4, 2, 2, ['n', 'n_log_b_a', 'f_n', 'time_complexity']),
    (4, 2, 3, ['n', 'n_log_b_a', 'f_n', 'time_complexity']),
])
def test_calculate_plot_data_structure(a, b, k, expected_keys):
    plot_data = calculate_plot_data(a, b, k)
    
    # Test the structure of the returned dictionary
    assert isinstance(plot_data, dict), "calculate_plot_data should return a dictionary."
    for key in expected_keys:
        assert key in plot_data, f"Key {key} is missing in the result."

@pytest.mark.parametrize("a,b,k", [
    (1, 2, 0),
    (2, 2, 1),
    (7, 2, 2),
    (3, 2, 1),
    (4, 2, 1),
    (4, 2, 2),
    (4, 2, 3),
])
def test_calculate_plot_data_length(a, b, k):
    plot_data = calculate_plot_data(a, b, k)
    
    # Test the lengths of the lists inside the dictionary
    n_length = len(plot_data['n'])
    for key in ['n_log_b_a', 'f_n', 'time_complexity']:
        assert len(plot_data[key]) == n_length, f"Length of {key} does not match length of 'n'."

@pytest.mark.parametrize("a,b,k,expected_first_value_of_fn,expected_first_value_of_n_log_b_a", [
    (2, 2, 0, 1, 1),  # f(n) should start at 1 for k=0, and n_log_b_a should start at 1 when n=1.
    (2, 2, 1, 1, 1),  # f(n) should start at 1 for k=1, and n_log_b_a should start at 1 when n=1.
    (9, 2, 0, 1, 1),  # f(n) should start at 1 for k=0, and n_log_b_a should start at 1 when n=1.
])
def test_calculate_plot_data_values(a, b, k, expected_first_value_of_fn, expected_first_value_of_n_log_b_a):
    plot_data = calculate_plot_data(a, b, k)
    
    # Test specific values within the lists
    assert np.isclose(plot_data['f_n'][0], expected_first_value_of_fn), f"First value of f(n) does not match expected for a={a}, b={b}, k={k}."
    assert np.isclose(plot_data['n_log_b_a'][0], expected_first_value_of_n_log_b_a), f"First value of n_log_b_a does not match expected for a={a}, b={b}, k={k}."

@pytest.mark.parametrize("a,b,k", [
    (1, 2, 0),
    (2, 2, 1),
    (7, 2, 2),
    (3, 2, 1),
    (4, 2, 1),
    (4, 2, 2),
    (4, 2, 3),
])
def test_calculate_plot_data_monotonicity(a, b, k):
    plot_data = calculate_plot_data(a, b, k)
    
    # Test that the lists are monotonically increasing where expected
    assert all(x <= y for x, y in zip(plot_data['n'], plot_data['n'][1:])), "'n' should be monotonically increasing."
    assert all(x <= y for x, y in zip(plot_data['time_complexity'], plot_data['time_complexity'][1:])), "'time_complexity' should be monotonically increasing."
