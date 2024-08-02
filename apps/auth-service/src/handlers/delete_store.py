import json
from .lib.util.delete_item_from_db import delete_item_from_db
from .lib.util.returns import return_json

def handler(event, context):
    id = event["pathParameters"]["id"]
    try:
        delete_item_from_db("StoresTable", id)
        return return_json({}, 202)
    except:
        return return_json({"message": "failed to delete store"}, 400)
