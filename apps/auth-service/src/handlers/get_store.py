from .lib.util.returns import return_json
from .lib.store import read_store

def handler(event, context):
    store_id = event["pathParameters"]["id"]
    try:
        store = read_store(store_id)
        if store is None:
            return return_json({}, 404)
        return return_json(store, 200)
    except Exception as e:
        print(e)
        return return_json({}, 400)
