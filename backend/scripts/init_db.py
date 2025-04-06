import os
import json
import boto3
from botocore.exceptions import ClientError

DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8000")
TABLE_NAME = "Algorithms"

# Get the absolute path to the directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=DYNAMODB_ENDPOINT_URL,
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "fakeMyKeyId"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "fakeSecretAccessKey")
)

def create_table_if_not_exists():
    try:
        dynamodb.meta.client.describe_table(TableName=TABLE_NAME)
        print(f"Table {TABLE_NAME} already exists.")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            print(f"Creating DynamoDB table: {TABLE_NAME}...")
            table = dynamodb.create_table(
                TableName=TABLE_NAME,
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "N"}],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
            )
            table.wait_until_exists()
            print(f"Table {TABLE_NAME} created.")
        else:
            raise

def seed_data():
    # Build an absolute path to algorithms_seed.json,
    # which lives one level up from scripts/
    json_file_path = os.path.join(SCRIPT_DIR, "..", "algorithms_seed.json")
    table = dynamodb.Table(TABLE_NAME)

    with open(json_file_path, "r") as f:
        items = json.load(f)

    for item in items:
        table.put_item(Item=item)
    print(f"Seeded {len(items)} items into {TABLE_NAME}.")

if __name__ == "__main__":
    create_table_if_not_exists()
    seed_data()
