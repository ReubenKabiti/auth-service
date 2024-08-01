import json
from .lib.stores import stores
from .lib.utils import find_by_id

def handler(event, context):
    path_params = event.get("pathParameters", {})
    store_id = path_params.get("id", None)

    store = find_by_id(stores, store_id)

    if store is None:
        return {
                "statusCode": 404,
                "body": {"message": f"Could not find store with id {store_id}"}
            }

    return {
            "statusCode": 200,
            "body": {"store": store}
        }
