from .lib.util.returns import return_json
import boto3 

table = boto3.resource("dynamodb").Table("ProductsTable")

def handler(event, context):
    store_id = event["pathParameters"]["id"]
    res = table.query(
        IndexName="storeId",
        KeyConditionExpression=boto3.dynamodb.conditions.Key("store_id").eq(store_id)
    )
    if not "Items" in res:
        return return_json({"message": "store doesn't exist"}, 404)
    items = res["Items"]
    return return_json({"items": items}, 200)
