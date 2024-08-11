import boto3
from uuid import uuid4 as uuid
from passlib.hash import pbkdf2_sha256
import json

table = boto3.resource("dynamodb").Table(os.environ.get("UsersTableName"))

def handler(event, context):
    body = json.loads(event.get("body"))

    username = body.get("username")
    email = body.get("email")
    fullname = body.get("fullname")

    password = body.get("password")

    hashed_pw = pbkdf2_sha256.hash(password)
    
    item = {
        "id": str(uuid()),
        "username": username,
        "fullname": fullname,
        "email": email,
        "password": hashed_pw,
    }

    table.put_item(Item=item)
    return {
        "statusCode": 201,
        "body": json.dumps({"id": item["id"]}),
    }
