import boto3
from uuid import uuid4 as uuid
from passlib.hash import pbkdf2_sha256
import json
import os
from .lib.table import table

def handler(event, context):
    body = json.loads(event.get("body"))

    username = body.get("username")
    email = body.get("email")
    fullname = body.get("fullname")

    password = body.get("password")

    hashed_pw = pbkdf2_sha256.hash(password)

    item = {
        "pk": f"USER#{str(uuid())}",
        "GSI1": email,
        "username": username,
        "fullname": fullname,
        "password": hashed_pw,
    }

    table.put_item(Item=item)
    return {
        "statusCode": 201,
        "body": json.dumps({"pk": item["pk"]}),
    }
