import json
from .cedar_text import schema, policies
from .utils import find_by_id


def generate_policy(principal_id, effect, resource):
    res = { "principalId": principal_id }
    if (effect and resource):
        doc = { "Version": "2012-10-17", "Statement": [] }
        s1 = {"Action": "execute-api:Invoke", "Effect": effect, "Resource": resource}
        doc["Statement"] = [s1]
        res["policyDocument"] = doc

    res_json = json.dumps(res)
    return res_json

def handler(event, context):
    token = event["authorizationToken"]
    try:
        id = int(token)
        user = find_by_id(users, id)
        if user is None:
           return json.loads(generate_policy("user", "Deny", event["methodArn"]))
        return json.loads(generate_policy("user", "Allow", event["methodArn"]))
    except:
       return json.loads(generate_policy("user", "Deny", event["methodArn"]))
