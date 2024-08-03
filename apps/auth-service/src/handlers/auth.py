import json
import boto3
import jwt
import re

from cedarpy import is_authorized,  Decision

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

def extract_method_and_resource(event):
    method_arn = event["methodArn"]
    
    arn_parts = method_arn.split(":")
    api_gateway_part = arn_parts[5]  

    api_gateway_parts = api_gateway_part.split("/")
    stage = api_gateway_parts[1]
    http_method = api_gateway_parts[2]
    resource_path = "/".join(api_gateway_parts[3:])

    return http_method, resource_path

def generate_cedar_policies(event):
    policies = r"""
    permit (
        principal,
        action,
        resource
    );
    // prevent someone from creating a store for someone else
    forbid (
        principal,
        action == Action::"POST",
        resource == Api::"/store"
    ) unless { principal == resource.owner };

    """
    return policies

def match_request(event):
    _, resource = extract_method_and_resource(event)
    patterns = {
        r"(signup)/?": "/signup",
        r"(login)/?": "/login",
        r"(product)/?": "/product",
        r"(product)/([0-9a-z\-]+)/?": "/product/{id}",
        r"(store)/?": "/store",
        r"(store)/([0-9a-z\-]+)/?": "/store/{id}",
        r"(store)/([0-9a-z\-]+)/(delete)/?": "/store/{id}/delete",
        r"(store)/([0-9a-z\-]+)/(products)/?": "/store/{id}/products",
    }

    for pattern in patterns.keys():
        result = re.findall(pattern, resource)
        if result:
            return result, patterns[pattern]

    return None, None


def generate_cedar_entities(event, user):
    # the way the entities are generated depends on the resource being accessed
    entities = []

    method, _ = extract_method_and_resource(event)
    _, resource = match_request(event)
    print(f"matched resource {resource}")

    if resource == "/store":
        if method == "POST":
            p = {
                "uid": {
                    "type": "User",
                    "id": user["id"]
                },
                "parents": [],
                "attrs": {}
            }
            r = {
                "uid": {
                    "type": "Api",
                    "id": "/store"
                },
                "parents": [],
                "attrs": {
                    "owner": { "__entity": {
                        "type": "User",
                        "id": user["id"]
                    }}
                }
            }
    return entities

def generate_cedar_request(event, user):
    method, _ = extract_method_and_resource(event)
    _, resource = match_request(event)

    p = f"User::\"{user['id']}\""
    a = f"Action::\"{method}\""
    r = f"Api::\"{resource}\""
    return {
        "principal": p,
        "action": a,
        "resource": r,
        "context": {}
    }

def evalute_cedar(p, e, r):
    decision = is_authorized(r, p, e)
    return Decision.Allow == decision.decision

def handler(event, context):
    token = event["authorizationToken"]
    try:
        user = jwt.decode(token, "author", algorithms=["HS256"])
        if user is None:
           return json.loads(generate_policy("user", "Deny", event["methodArn"]))
        
        policies = generate_cedar_policies(event)
        entities = generate_cedar_entities(event, user)
        request = generate_cedar_request(event, user)
        print(f"policies = {policies}")
        print(f"entities = {entities}")
        print(f"request = {request}")
        decision = evalute_cedar(policies, entities, request)
        print(f"decision = {decision}")
        if decision:
            return json.loads(generate_policy(user["id"], "Allow", event["methodArn"], context=user))
        return json.loads(generate_policy("user", "Deny", event["methodArn"]))
    except Exception as e:
        print(e)
        return json.loads(generate_policy("user", "Deny", event["methodArn"]))
