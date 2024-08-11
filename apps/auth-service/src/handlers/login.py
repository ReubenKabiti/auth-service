import jwt
import boto3
import json
from passlib.hash import pbkdf2_sha256
import datetime
import os

table = boto3.resource("dynamodb").Table(os.environ.get("UsersTableName"))

def handler(event, context):
    body = json.loads(event.get("body"))
    email = body.get("email")
    password = body.get("password")

    error_msg = "Incorrect email or password"

    res = table.query(
        IndexName="emailIndex",
        KeyConditionExpression=boto3.dynamodb.conditions.Key("email").eq(email)
    )

    if not "Items" in res:
        return {
            "statusCode": 400,
            "body": json.dumps({"message":  error_msg}),
        }

    user = res.get("Items")[0]

    if not pbkdf2_sha256.verify(password, user["password"]):
        return {
            "statusCode": 400,
            "body": json.dumps({"message":  error_msg}),
        }

    exp = datetime.datetime.now() + datetime.timedelta(3600*24*3) # jwt token expires after 3 days

    claims = { "id": user.get("id"), "username": user.get("username"), "email": email, "exp": exp}
    token = jwt.encode(claims, "author")

    return {
        "statusCode": 200,
        "body": json.dumps({"token": token}),
    }

