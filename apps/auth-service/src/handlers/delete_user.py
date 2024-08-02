import json
from .lib.util.delete_item_from_db import delete_item_from_db
from .lib.util.returns import return_json

def handler(event, context):
    id = event["pathParameters"]["id"]
    try:
        delete_item_from_db("UsersTable", id)
        return return_json(status_code=202)
    except:
        return return_json({"message": "id provided does not belong to any user"}, 404)
