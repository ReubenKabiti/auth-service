import json
from .lib.util.returns import return_json
from .lib.products import delete_product, find_products_from_store
import boto3

table = boto3.resource("dynamodb").Table("StoresTable")

def handler(event, context):
    id = event["pathParameters"]["id"]
    try:
        products = fin
        return return_json({}, 202)
    except:
        return return_json({"message": "failed to delete store"}, 400)
