import json
import boto3
import jwt
import re
import os

from .lib.get_user_policies import get_user_policies

from cedarpy import is_authorized, Decision

def extract_resources_from_policy(policies):
    resource_pattern = r'(resource)\s==\sApi::"([0-9a-zA-Z_\-/\*]+)"'
    regex_resource = {}
    slug_pattern = r"[0-9a-zA-Z\-]+"

    for policy in policies:
        matches = re.findall(resource_pattern, policy)
        for match in matches:
            _, resource = match
            regex = resource.replace("*", slug_pattern)
            regex = f"{regex}/?"
            regex_resource[regex] = resource
    return regex_resource



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

    return http_method, f"/{resource_path}"

def match_request(policies, resource_raw):
    regex_resource = extract_resources_from_policy(policies)
    print(regex_resource, resource_raw)
    for regex in regex_resource:
        if re.match(regex, resource_raw):
            return regex_resource[regex]


def generate_cedar_entities():
    entities = []
    return entities

def generate_cedar_request(user, method, resource):

    p = f"User::\"{user['pk']}\""
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

        policies = get_policies(user["pk"])
        entities = generate_cedar_entities()
        method, resource_raw = extract_method_and_resource(event)
        resource = match_request(policies, resource_raw)
        policies = "\n".join(policies)

        request = generate_cedar_request(user, method, resource)

        print(f"policies = {policies}")
        print(f"entities = {entities}")
        print(f"request = {request}")

        if resource is None:
           return json.loads(generate_policy("user", "Deny", event["methodArn"]))

        decision = evalute_cedar(policies, entities, request)

        print(f"decision = {decision}")
        if decision:
        # if True: # ignore policies for now
            return json.loads(generate_policy(user["pk"], "Allow", event["methodArn"], context=user))
        return json.loads(generate_policy("user", "Deny", event["methodArn"]))
    except Exception as e:
        print(e)
        return json.loads(generate_policy("user", "Deny", event["methodArn"]))
