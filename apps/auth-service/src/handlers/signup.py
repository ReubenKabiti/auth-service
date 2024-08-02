import boto3
import bcrypt
from uuid import uuid4 as uuid
import json

db = boto3.resource("dynamodb")
table = db.Table("UsersTable")

def handler(event, context):
    body = event.get("body")
    username = body.get("username")
    email = body.get("email")
    password = body.get("password")
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    item = {
        "id": str(uuid()),
        "username": username,
        "email": email,
        "password": hashed_pw
    }

    table.put_item(Item=item)
    return {
        "statusCode": 201,
        "body": json.dumps({}),
    }
