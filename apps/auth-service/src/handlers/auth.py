import json
from .cedar_text import schema, policies
import boto3
import jwt

def generate_policy(principal_id, effect, resource, context=None):
    res = { "principalId": principal_id }
    if (effect and resource):
        doc = { "Version": "2012-10-17", "Statement": [] }
        s1 = {"Action": "execute-api:Invoke", "Effect": effect, "Resource": resource}
        doc["Statement"] = [s1]
        res["policyDocument"] = doc
    if not context is None:
        res["context"] = context
    res_json = json.dumps(res)
    return res_json

def is_token_valid(token):
    print(f"token is {token}")
    try:
        claims = jwt.decode(token, "author")
        return claims
    except:
        return False

def handler(event, context):
    token = event["authorizationToken"]
    try:
        if user := is_token_valid(token) == False:
           return json.loads(generate_policy("user", "Deny", event["methodArn"]))
        return json.loads(generate_policy(user["id"], "Allow", event["methodArn"], context=user))
    except:
       return json.loads(generate_policy("user", "Deny", event["methodArn"]))
