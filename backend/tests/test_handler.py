# backend/tests/test_handler.py

from backend.handler import run

def test_handler_lambda_event():
    event = {
        "resource": "/api/algorithms",
        "path": "/api/algorithms",
        "httpMethod": "GET",
        "headers": {},
        "multiValueHeaders": {},
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "requestContext": {
            "resourcePath": "/api/algorithms",
            "httpMethod": "GET",
            "path": "/api/algorithms",
            "accountId": "123456789012",
            "stage": "test",
            "requestId": "fake-request-id",
            "identity": {
                "sourceIp": "127.0.0.1",
                "userAgent": "pytest"
            },
            "apiId": "test-api"
        },
        "body": None,
        "isBase64Encoded": False
    }
    response = run(event, None)
    assert response["statusCode"] == 200
