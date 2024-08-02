import jwt
import boto3
import json
from passlib.hash import pbkdf2_sha256
from .lib.util.returns import return_json

db = boto3.resource("dynamodb")
table = db.Table("UsersTable")

def handler(event, context):
    body = json.loads(event.get("body"))
    email = body.get("email")
    password = body.get("password")

    error_msg = "Incorrect username or password"

    res = table.query(
        IndexName="emailIndex",
        KeyConditionExpression=boto3.dynamodb.conditions.Key("email").eq(email)
    )

    if not "Items" in res:
        return return_json({"message": error_msg}, 404)

    user = res.get("Items")[0]

    if not pbkdf2_sha256.verify(password, user["password"]):
        return return_json({"message": error_msg}, 404)

    claims = { "id": user.get("id"), "username": user["username"], "email": email }
    token = jwt.encode(claims, "author")
    return return_json({"token": token}, 200)
