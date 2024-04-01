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
    assert 'plot_data' in response.data

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

@pytest.mark.django_db
def test_algorithm_list_view_order():
    client = APIClient()
    # Ensure the algorithms are created in a certain order
    first_algorithm = Algorithm.objects.create(name="Algorithm A", description="First Algorithm", python_code="def algorithm_a():pass")
    second_algorithm = Algorithm.objects.create(name="Algorithm B", description="Second Algorithm", python_code="def algorithm_b():pass")

    response = client.get('/api/algorithms/')
    assert response.status_code == 200
    assert len(response.data) == 2

    # Verify th order by ID or any other attribute that reflects creation order
    assert response.data[0]['id'] == first_algorithm.id
    assert response.data[1]['id'] == second_algorithm.id

@pytest.mark.django_db
def test_algorithm_order_after_modification():
    client = APIClient()
    # Create two algorithms
    first_algorithm = Algorithm.objects.create(name="Algorithm C", description="C Algorithm", python_code="def algorithm_c(): pass")
    second_algorithm = Algorithm.objects.create(name="Algorithm D", description="D Algorithm", python_code="def algorithm_d(): pass")

    # Modify the first algorithm
    Algorithm.objects.filter(id=first_algorithm.id).update(name="Algorithm C Updated")

    response = client.get('/api/algorithms/')
    assert response.status_code == 200
    assert len(response.data) == 2

    # Check if the order is still by creation time (ID)
    assert response.data[0]['id'] == first_algorithm.id
    assert response.data[0]['name'] == "Algorithm C Updated"
    assert response.data[1]['id'] == second_algorithm.id

    # Modify the second algorithm
    Algorithm.objects.filter(id=second_algorithm.id).update(name="Algorithm D Updated")

    response = client.get('/api/algorithms/')
    assert response.status_code == 200
    assert len(response.data) == 2

    # Check if the order is by ID again
    assert response.data[1]['id'] == second_algorithm.id
    assert response.data[1]['name'] == "Algorithm D Updated"
    assert response.data[0]['id'] == first_algorithm.id
