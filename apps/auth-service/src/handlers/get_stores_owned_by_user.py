import boto3
from .lib.util.returns import return_json

table = boto3.resource("dynamodb").Table("StoresTable")

def handler(event, context):
    user_id = event["pathParameters"]["id"]

    res = table.query(
        IndexName="userId",
        KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(user_id)
    )
    if not "Items" in res:
        return return_json({"message": "user doesn't exist"}, 404)
    items = res["Items"]
    return return_json({"items": items}, 200)
