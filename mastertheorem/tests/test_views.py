# mastertheorem/tests/test_views.py

import pytest
from rest_framework.test import APIClient
from mastertheorem.models import Algorithm

@pytest.mark.django_db
def test_evaluate_master_theorem_api_view_success():
    client = APIClient()
    data = {'a': 2, 'b': 2, 'k': 1}
    response = client.post('/api/evaluate/', data, format='json')
    assert response.status_code == 200
    assert 'complexity' in response.data
    assert 'case' in response.data
    assert 'plot_url' in response.data

@pytest.mark.django_db
def test_evaluate_master_theorem_api_view_failure():
    client = APIClient()
    invalid_data = {'a': -1, 'b': 0, 'k': -1}
    response = client.post('/api/evaluate/', invalid_data, format='json')
    assert response.status_code == 400
    assert 'a' in response.data
    assert 'b' in response.data
    assert 'k' in response.data
    
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