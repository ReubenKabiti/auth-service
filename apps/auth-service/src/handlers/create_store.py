import boto3
import json
from uuid import uuid4 as uuid
from .lib.util.returns import return_json

table = boto3.resource("dynamodb").Table("StoresTable")

def handler(event, context):
    try:
        user = event["requestContext"]["authorizer"]
        user_id = user["id"]
        body = json.loads(event.get("body"))
        store_name = body["store_name"]
        item = {
            "id": str(uuid()),
            "store_name": store_name,
            "owner": user_id,
        }
        table.put_item(Item=item)
        return return_json({"store_id": item["id"]}, 201)
    except:
        return return_json({"message": "failed to create store"}, 400)
