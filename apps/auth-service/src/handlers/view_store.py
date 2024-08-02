import json

def handler(event, context):
    path_params = event.get("pathParameters", {})
    store_id = path_params.get("id", None)

    store = {
        "name": "my store",
        "id": store_id
    }

    return {
            "statusCode": 200,
            "body": json.dumps({"store": store}),
        }
