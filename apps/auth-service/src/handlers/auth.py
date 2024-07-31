import json
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
    res = {}
    if token == "Allow":
        res = generate_policy("user", "Allow", event["methodArn"])
    elif token == "deny":
        res = generate_policy("user", "Deny", event["methodArn"])
    try:
        json.loads(res)
    except BaseException:
        return "unauthorized"
