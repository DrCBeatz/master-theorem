# test_master_theorem.py

import pytest
from master_theorem import evaluate_master_theorem
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
