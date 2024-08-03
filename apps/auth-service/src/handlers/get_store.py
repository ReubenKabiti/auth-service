import boto3
from .lib.util.returns import return_json
table = boto3.resource("dynamodb").Table("StoresTable")

def handler(event, context):
    store_id = event["pathParameters"]["id"]
    try:
        response = table.get_item(Key={"id": store_id})
        store = response.get("Item")
        print(f"found store {store}")
        if store is None:
            return return_json({}, 404)
        return return_json(store, 200)
    except Exception as e:
        print(e)
        return return_json({}, 400)
