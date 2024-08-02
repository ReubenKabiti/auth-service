import boto3
import json
from uuid import uuid4 as uuid
from .lib.util.returns import return_json

table = boto3.resource("dynamodb").Table("ProductsTable")

def handler(event, context):
    store_id = event["pathParameters"]["id"]
    body = json.loads(event["body"])
    product_name = body["name"]
    product_price = body["price"]
    product_quantity = body["quantity"]

    item = {
        "id": str(uuid()),
        "name": product_name,
        "price": product_price,
        "quantity": product_quantity,
        "store": store_id
    }

    try:
        table.put_item(Item=item)
        return return_json(item, 201)
    except:
        return return_json({"message": "could not create product"}, 400)
