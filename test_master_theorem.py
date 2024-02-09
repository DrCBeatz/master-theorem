# test_master_theorem.py

import pytest
from master_theorem import master_theorem
from sympy import symbols

@pytest.mark.parametrize("a, b, f_n, expected", [
    (2, 2, 1, "Case 1: T(n) = Theta(log n)"), # e.g. Binary Search
    (2, 2, symbols('n'), "Case 2: T(n) = Theta(n^1 log(n))"), # e.g. Merge Sort
    (2, 2, symbols('n')**2, "Case 3: T(n) = Theta(n**2)"),
])
def test_master_theorem(a, b, f_n, expected):
    n = symbols('n')
    assert master_theorem(a, b, f_n, n) == expected
