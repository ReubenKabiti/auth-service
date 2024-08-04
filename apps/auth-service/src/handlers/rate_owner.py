import boto3
import json
from .lib.util.returns import return_json

table = boto3.resource("dynamodb").Table("UsersTable")

def handler(event, context):
    user_id = event["pathParameters"]["id"]
    rating = json.loads(event["body"])["rating"]
    try:
        # get the user object
        user = table.get_item(Key={"id": user_id}).get("Item")
        if user is None:
            return return_json({"message": "user not found!"}, 404)
        old_rating = user["rating"]
        old_rating.append(rating)


        table.update_item(
            Key={"id": user_id},
            UpdateExpression="SET #rating = :rating",
            ExpressionAttributeNames={
                "#rating": "rating",
            },
            ExpressionAttributeValues={
                ":rating": old_rating,
            }
        )

        return return_json({}, 200)

    except Exception as e:
        print(e)
        return return_json({}, 400)

