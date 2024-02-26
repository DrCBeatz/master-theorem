# mastertheorem/tests/test_models.py

import pytest
from django.core.exceptions import ValidationError
from mastertheorem.models import Algorithm

@pytest.mark.django_db
def test_algorithm_creation():
    # Test creating and saving an Algorithm instance
    algorithm = Algorithm(
        name="Binary Search",
        a=1,
        b=2,
        k=0,
        description="A search algorithm...",
        python_code="def binary_search(arr,x):...",
        case="Case 2",
        time_complexity="O(log n)"
    )
    algorithm.save()

    # Fetch the saved algorithm from the database
    fetched_algorithm = Algorithm.objects.get(name="Binary Search")

    # Assert that the ftched algorithm has the correct attributes
    assert fetched_algorithm.a == 1
    assert fetched_algorithm.b == 2
    assert fetched_algorithm.k == 0
    assert fetched_algorithm.description.startswith("A search algorithm")
    assert fetched_algorithm.python_code.startswith("def binary_search")
    assert fetched_algorithm.case == "Case 2"
    assert fetched_algorithm.time_complexity == "O(log n)"

@pytest.mark.django_db
def test_algorithm_min_values():
    # Attempt to create an Algorithm with  values below the minimum allowed
    algorithm = Algorithm(name="Test Algorithm", a=-1, b=1, k=-1, p=-1)

    # Expect a ValidationErro rdue tot eh MinValueValidator constraints
    with pytest.raises(ValidationError):
        algorithm.full_clean() # This method triggers the model's validators

@pytest.mark.django_db
def test_algorithm_optional_fields():
    # Test creating an algorithm with optional fields left blank
    algorithm = Algorithm(
        name="Optional Fields Test",
        a=2,
        b=2,
        k=1,
        description="Testing optional fields."
    )
    algorithm.save()

    # Fetch and assert that optional fields are indeed blank/null
    fetched_algorithm = Algorithm.objects.get(name="Optional Fields Test")
    assert fetched_algorithm.case is None
    assert fetched_algorithm.time_complexity is None
    assert fetched_algorithm.complexity_analysis is None

