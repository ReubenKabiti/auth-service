import boto3
from uuid import uuid4 as uuid
from passlib.hash import pbkdf2_sha256
import json
from .lib.util.returns import return_json

table = boto3.resource("dynamodb").Table("UsersTable")

def handler(event, context):
    body = json.loads(event.get("body"))
    username = body.get("username")
    email = body.get("email")
    password = body.get("password")
    hashed_pw = pbkdf2_sha256.hash(password)
    
    item = {
        "id": str(uuid()),
        "username": username,
        "email": email,
        "password": hashed_pw,
        "rating": [],
        "role": "User",
    }

    table.put_item(Item=item)

    return return_json({"id": item["id"]}, 201)
