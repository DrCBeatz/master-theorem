import pytest
from rest_framework.test import APIClient
from mastertheorem.models import Algorithm

@pytest.mark.django_db
def test_algorithm_list_view():
    # Set up
    client = APIClient()
    Algorithm.objects.create(name="Binary Search", description="Binary Search Description", python_code="def binary_search(): pass")
    Algorithm.objects.create(name="Merge Sort", description="Merge Sort Description", python_code="def merge_sort():pass")

    # Make a GET request to the algorithm list endpoint
    response = client.get('/api/algorithms/')

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Check the length of th response data to ensure both algorithms are returned
    assert len(response.data) == 2

    # Additional checks can be made to verify the content of the response
    assert response.data[0]['name'] == "Binary Search"
    assert response.data[0]['description'] == "Binary Search Description"
    assert response.data[0]['python_code'].startswith('def binary_search') == True
    assert response.data[1]['name'] == "Merge Sort"
    assert response.data[1]['description'] == "Merge Sort Description"
    assert response.data[1]['python_code'].startswith('def merge_sort') == True