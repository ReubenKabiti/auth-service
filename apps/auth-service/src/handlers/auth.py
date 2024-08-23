import json
import boto3
import jwt
import re
import os

from .lib.get_user_policies import get_user_policies

from cedarpy import is_authorized, Decision

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

def generate_cedar_entities():
    entities = []
    return entities

def generate_cedar_request(event, user):
    method, resource = extract_method_and_resource(event)

    p = f"User::\"{user['id']}\""
    a = f"Action::\"{method}\""
    r = f"Api::\"{resource}\""

    return {
        "principal": p,
        "action": a,
        "resource": r,
        "context": {}
    }

def get_policies(user_id):
    return get_user_policies(user_id)

def evalute_cedar(p, e, r):
    decision = is_authorized(r, p, e)
    return Decision.Allow == decision.decision

def handler(event, context):
    print(event, context)
    token = event["authorizationToken"]
    try:
        user = jwt.decode(token, "author", algorithms=["HS256"])
        if user is None:
           return json.loads(generate_policy("user", "Deny", event["methodArn"]))
        policies = "\n".join(get_policies(user["id"]))
        entities = generate_cedar_entities()
        request = generate_cedar_request(event, user)
        print(f"policies = {policies}")
        print(f"entities = {entities}")
        print(f"request = {request}")
        decision = evalute_cedar(policies, entities, request)
        print(f"decision = {decision}")
        # if decision:
        if True: # ignore policies for now
            return json.loads(generate_policy(user["id"], "Allow", event["methodArn"], context=user))
        return json.loads(generate_policy("user", "Deny", event["methodArn"]))
    except Exception as e:
        print(e)
        return json.loads(generate_policy("user", "Deny", event["methodArn"]))
