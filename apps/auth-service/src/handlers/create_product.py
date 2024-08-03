import boto3
import json
from uuid import uuid4 as uuid
from .lib.util.returns import return_json

table = boto3.resource("dynamodb").Table("ProductsTable")

def handler(event, context):
    body = json.loads(event["body"])
    product_name = body["name"]
    product_price = body["price"]
    product_quantity = body["quantity"]
    store_id = body["store_id"]

    item = {
        "id": str(uuid()),
        "store_id": store_id,
        "name": product_name,
        "price": product_price,
        "quantity": product_quantity,
    }

    try:
        table.put_item(Item=item)
        return return_json(item, 201)
    except Exception as e:
        print(e)
        return return_json({"message": "could not create product"}, 400)
