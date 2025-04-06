# backend/scripts/init_db.py

import os
import json
import time
import boto3
from botocore.exceptions import ClientError

DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8000")
TABLE_NAME = "Algorithms"

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=DYNAMODB_ENDPOINT_URL,
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "fakeMyKeyId"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "fakeSecretAccessKey")
)

def create_table_if_not_exists():
    """
    Checks if a table with TABLE_NAME exists.
    If not, create it with 'id' as the partition key (example).
    """
    try:
        dynamodb.meta.client.describe_table(TableName=TABLE_NAME)
        print(f"Table {TABLE_NAME} already exists.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Creating DynamoDB table: {TABLE_NAME}...")
            table = dynamodb.create_table(
                TableName=TABLE_NAME,
                KeySchema=[
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'N'  # 'S' for string, 'N' for number
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.wait_until_exists()
            print(f"Table {TABLE_NAME} created.")
        else:
            raise

def seed_data(json_file_path="algorithms_seed.json"):
    """Load items from the given JSON file and put them into the table."""
    table = dynamodb.Table(TABLE_NAME)
    with open(json_file_path, "r") as f:
        items = json.load(f)

    for item in items:
        table.put_item(Item=item)
    print(f"Seeded {len(items)} items into {TABLE_NAME}.")

if __name__ == "__main__":
    create_table_if_not_exists()
    seed_data()
