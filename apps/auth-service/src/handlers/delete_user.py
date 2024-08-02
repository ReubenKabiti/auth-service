import boto3
import json

db = boto3.resource("dynamodb")
table = db.Table("UsersTable")

def handler(event, context):
    body = json.loads(event.get("body"))
    id = body.get("id")

    try:
        table.delete_item(Key={
            "id": id
        })

        return {
            "statusCode": 202,
            body: json.dumps({}),
        }
    except:
        return {
            "statusCode": 404,
            body: json.dumps({"message": "id provided does not belong to any user"}),
        }
