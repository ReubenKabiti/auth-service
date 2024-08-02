import boto3
from .lib.util.returns import return_json
table = boto3.resource("dynamodb").Table("ProductsTable")

def handler(event, context):
    id = event["pathParameters"]["id"]
    try:
        product = table.get_item({"id": id})
        if product is None:
            return return_json({"message": "product not found"}, 404)
        return return_json({"product": product}, 200)
    except:
        return return_json({"message": "product not found"}, 404)
