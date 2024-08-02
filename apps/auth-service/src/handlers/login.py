import jwt
import boto3
import json
from passlib.hash import pbkdf2_sha256

db = boto3.resource("dynamodb")
table = db.Table("UsersTable")

SECRET = "4687180f-fa3c-43af-9ae8-a7d90016b4ce" # just a placeholder

def handler(event, context):
    body = json.loads(event.get("body"))
    email = body.get("email")
    password = body.get("password")

    res = table.query(
        IndexName="emailIndex",
        KeyConditionExpression=boto3.dynamodb.conditions.Key("email").eq(email)
    )

    if not "Items" in res:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Incorrect username or password"}),
        }

    user = res.get("Items")[0]

    if not pbkdf2_sha256.verify(password, user["password"]):
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Incorrect username or password"}),
        }

    claims = { "id": user.get("id"), "username": user["username"], "email": email }
    token = jwt.encode(claims, SECRET)
    return {
            "statusCode": 200,
            "body": json.dumps({"token": token})
    }
