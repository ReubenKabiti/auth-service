from .lib.store import read_stores_from_user
from .lib.util.returns import return_json

def handler(event, context):
    user_id = event["pathParameters"]["id"]

    res = read_stores_from_user(user_id)

    if not "Items" in res:
        return return_json({"message": "user doesn't exist"}, 404)
    items = res["Items"]
    return return_json({"stores": items}, 200)
