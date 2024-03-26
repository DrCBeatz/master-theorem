# mastertheorem/tests/test_master_theorem.py

import pytest
from mastertheorem.master_theorem import evaluate_master_theorem, calculate_plot_data
import numpy as np

CASE_1 = f"Case 1: Θ(n<sup>log<sub>b</sub>(a)</sup>)"
CASE_2 = f"Case 2: Θ(n<sup>k</sup> log n)"
CASE_3 = f"Case 3: Θ(n<sup>k</sup>)"

@pytest.mark.parametrize("a,b,k,expected_start,expected_case,description,expected_error_message", [
    # Valid test cases, ensuring all parameters are integers
    (4, 2, 1, "Θ(n<sup>2</sup>)", CASE_1, "Generic algorithm - Case 1 (faster growth of recursive part)", None),
    (4, 2, 2, "Θ(n<sup>2</sup> log n)", CASE_2, "Generic algorithm - Case 2 (balanced growth)", None),
    (4, 2, 3, "Θ(n<sup>3</sup>)", CASE_3, "Generic algorithm - Case 3 (faster growth of non-recursive part)", None),
    (2, 2, 1, "Θ(n log n)", CASE_2, "Merge Sort", None),
    (7, 2, 2, "Θ(n<sup>log<sub>2</sub>(7)</sup>)", CASE_1, "Strassen's Matrix Multiplication", None),
    (1, 2, 0, "Θ(log n)", CASE_2, "Binary Search", None),
    (3, 2, 1, "Θ(n<sup>log<sub>2</sub>(3)</sup>)", CASE_1, "Karatsuba's Algorithm", None),
    # Tests for handling invalid input gracefully
    (0, 2, 1, "Error", "Error", "Zero subproblems - expected error", "Parameter 'a' must be greater than 0."),
    (2, 1, 1, "Error", "Error", "Division by 1 - expected error", "Parameter 'b' must be greater than 1 to ensure the problem size is reduced."),
    (-1, 2, 1, "Error", "Error", "Negative subproblems - expected error", "Parameter 'a' must be greater than 0."),

])
def test_master_theorem_cases(a: int, b: int, k: int, expected_start: str, expected_case: str, description: str, expected_error_message: str) -> None:
    if expected_case == "Error":
        with pytest.raises(ValueError, match=expected_error_message):
            evaluate_master_theorem(a, b, k)
    else:
        complexity, case, recurrence_relation, _ = evaluate_master_theorem(a, b, k)
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

@pytest.mark.parametrize("a,b,k,expected_recurrence_relation", [
    (1, 2, 0, "T(n) = 1T(n/2) + f(1)"),
    (2, 2, 1, "T(n) = 2T(n/2) + f(n<sup>1</sup>)"),
    (7, 2, 2, "T(n) = 7T(n/2) + f(n<sup>2</sup>)"),
    (3, 2, 1, "T(n) = 3T(n/2) + f(n<sup>1</sup>)"),
    (4, 2, 1, "T(n) = 4T(n/2) + f(n<sup>1</sup>)"),
    (4, 2, 2, "T(n) = 4T(n/2) + f(n<sup>2</sup>)"),
    (4, 2, 3, "T(n) = 4T(n/2) + f(n<sup>3</sup>)"),
])
def test_recurrence_relation_output(a: int, b: int, k: int, expected_recurrence_relation: str):
       _, _, recurrence_relation, _ = evaluate_master_theorem(a, b, k) 
       assert recurrence_relation == expected_recurrence_relation, f"Recurrence relation does not expected output for parameters a={a}, b={b}, k={k}"

@pytest.mark.parametrize("a,b,k,expected_regularity", [
    (4, 2, 3, True),  # Case 3, Regularity condition met.
    (10, 2, 3, False),  # Case 1, regularity condition not applicable.
    (8, 2, 3, False),  # Case 2, regularity condition not applicable.
    (9, 2, 3, False),  # Case 1, regularity condition not applicable.
    (2, 2, 1, False),  # Case 2, regularity condition not applicable.
    (1000, 10, 3, False),  # Case 3 with large values, testing the function's ability to correctly evaluate the regularity condition despite the significant value of 'a'. Regularity condition not met, demonstrating the function's robustness in handling extreme or non-intuitive scenarios within Case 3's criteria.
])
def test_regularity_condition(a: int, b: int, k: int, expected_regularity: bool):
    _, _, _, regularity_condition_met = evaluate_master_theorem(a, b, k)
    assert regularity_condition_met == expected_regularity, f"Regularity condition failed for parameters a={a}, b={b}, k={k}"
