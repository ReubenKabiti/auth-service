import json

users = [
        {
            "id": 0,
            "username": "alice",
        },
        {
            "id": 1,
            "username": "bob",
        },
        {
            "id": 2,
            "username": "eve",
        },
        {
            "id": 3,
            "username": "dave",
        },
        {
            "id": 4,
            "username": "steve",
        },
    ]

def find_user_with_id(users, id):
    for user in users:
        if user["id"] == id:
            return user

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
        user = find_user_with_id(users, id)
        if user is None:
           return json.loads(generate_policy("user", "Deny", event["methodArn"]))
        return json.loads(generate_policy("user", "Allow", event["methodArn"]))
    except:
       return json.loads(generate_policy("user", "Deny", event["methodArn"]))
