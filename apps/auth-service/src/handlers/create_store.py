import boto3
import json
from uuid import uuid4 as uuid

db = boto3.resource("dynamodb")
table = db.Table("StoresTable")

def handler(event, context):
    try:
        user = event["requestContext"]["authorizer"]
        user_id = user["id"]

        body = json.loads(event.body)
        store_name = body["store_name"]

        item = {
            "id": str(uuid()),
            "store_name": store_name
        }

        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "body": json.dumps({"store_id": item["id"]})
        }

    except:

        return {
                "statusCode": 400,
                "body": json.dumps({"message": "failed to create store"})
        }
