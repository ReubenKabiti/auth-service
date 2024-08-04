import json
from .lib.util.returns import return_json
from .lib.product import delete_product, find_products_from_store
import boto3

table = boto3.resource("dynamodb").Table("StoresTable")

def handler(event, context):
    id = event["pathParameters"]["id"]
    try:
        products = find_products_from_store(id)
        for product in products:
            delete_product(product["id"])
        table.delete_item(Key={"id": id})
        return return_json({}, 200)
    except Exception as e:
        print(e)
        return return_json({"message": "failed to delete store"}, 400)
