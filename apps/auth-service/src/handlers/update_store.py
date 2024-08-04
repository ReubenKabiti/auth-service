import boto3
import json
from .lib.util.returns import return_json

table = boto3.resource("dynamodb").Table("StoresTable")

def handler(event, context):
    update_fields = json.loads(event["body"])["update_fields"]
    store_id = event["pathParameters"]["id"]
    update_expressions = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    if "store_name" in update_fields:
        store_name = update_fields["store_name"]
        update_expressions.append("set #store_name = :store_name")
        expression_attribute_values[":store_name"] = store_name
        expression_attribute_names["#store_name"] = "store_name"

    update_expression = ",".join(update_expressions)
    try:
        response = table.update_item(
            Key={"id": store_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
        )

        return return_json({"store": response}, 200)
    except Exception as e:
        print(e)
        return return_json(status_code=400)

