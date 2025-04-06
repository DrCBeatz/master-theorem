# backend/tests/test_main.py

import os
import boto3
import pytest
from fastapi.testclient import TestClient
from backend.main import (
    app, 
    evaluate_master_theorem, 
    calculate_plot_data, 
    dynamodb )
from botocore.exceptions import ClientError

client = TestClient(app)

@pytest.fixture(scope="session")
def dynamodb_client():
    # Connect to local DynamoDB
    endpoint_url = os.getenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8000")
    client = boto3.client(
        "dynamodb",
        endpoint_url=endpoint_url,
        region_name="us-east-2",
        aws_access_key_id="fakeMyKeyId",
        aws_secret_access_key="fakeSecretAccessKey"
    )
    return client

@pytest.fixture(scope="function")
def setup_algorithms_table(dynamodb_client):
    """
    Creates the table at the start of the test, and tears it down at the end.
    If the table already exists, skip creation.
    """
    table_name = "Algorithms"

    existing_tables = dynamodb_client.list_tables()["TableNames"]
    if table_name not in existing_tables:
        dynamodb_client.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "N"},
            ],
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        # Wait for the table to be active
        waiter = dynamodb_client.get_waiter("table_exists")
        waiter.wait(TableName=table_name)
    
    yield
    # Optionally, clean up after test
    # dynamodb_client.delete_table(TableName=table_name)

def test_evaluate_master_theorem_valid():
    """
    Test a valid payload for /api/evaluate
    """
    # Example: a=2, b=2, k=1 => "Case 2: Θ(n^k log n)" => "Θ(n log n)"
    payload = {"a": 2, "b": 2, "k": 1}
    response = client.post("/api/evaluate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "complexity" in data
    assert "case" in data
    # Example checks based on known logic
    assert data["complexity"] == "Θ(n log n)"
    assert "Case 2" in data["case"]

@pytest.mark.parametrize(
    "a, b, k",
    [
        (0, 2, 1),  # a=0 should fail validation
        (2, 1, 0),  # b=1 should fail validation
    ]
)
def test_evaluate_master_theorem_invalid(a, b, k):
    response = client.post("/api/evaluate", json={"a": a, "b": b, "k": k})
    # with ge=1 for a, ge=2 for b => expect Pydantic 422
    assert response.status_code == 422

@pytest.mark.parametrize(
    "a, b, k, error_message",
    [
        (0, 2, 1, "Parameter 'a' must be greater than 0."),
        (2, 1, 1, "Parameter 'b' must be greater than 1."),
    ]
)
def test_evaluate_master_theorem_exceptions(a, b, k, error_message):
    with pytest.raises(ValueError) as exc_info:
        evaluate_master_theorem(a, b, k)
    assert str(exc_info.value) == error_message

@pytest.mark.parametrize(
    "a,b,k,expected_case,expected_complexity",
    [
        (8, 2, 1, "Case 1", "Θ(n<sup>3</sup>)"),
        (2, 2, 1, "Case 2", "Θ(n log n)"),
        (1, 2, 2, "Case 3", "Θ(n<sup>2</sup>)"),
    ]
)
def test_evaluate_master_theorem_all_cases(a, b, k, expected_case, expected_complexity):
    payload = {"a": a, "b": b, "k": k}
    response = client.post("/api/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert expected_case in data["case"]
    assert data["complexity"] == expected_complexity

@pytest.mark.parametrize(
    "a, b, k",
    [
        (4, 2, 1),  # log_b_a > k (Case 1)
        (2, 2, 1),  # log_b_a == k (Case 2)
        (1, 2, 2),  # log_b_a < k (Case 3)
        (1, 2, 0),  # k == 0 (Edge case)
    ]
)
def test_calculate_plot_data_branches(a, b, k):
    plot_data = calculate_plot_data(a, b, k)
    assert "n" in plot_data
    assert "f_n" in plot_data
    assert "time_complexity" in plot_data
    assert len(plot_data["n"]) == len(plot_data["f_n"]) == len(plot_data["time_complexity"])

def test_get_algorithms_dynamodb_failure(monkeypatch):
    # Mock the dynamodb.Table method itself
    def mock_table(*args, **kwargs):
        class MockTable:
            def scan(self):
                raise ClientError({"Error": {"Message": "Mock DynamoDB failure"}}, "scan")
        return MockTable()

    monkeypatch.setattr(dynamodb, "Table", mock_table)

    response = client.get("/api/algorithms")
    assert response.status_code == 500
    assert "Mock DynamoDB failure" in response.json()["detail"]