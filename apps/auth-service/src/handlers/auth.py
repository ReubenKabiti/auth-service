import json
import boto3
import jwt
import re
import os

from lib.resource_creation import get_all_policies

from cedarpy import is_authorized, Decision

s3 = boto3.client("s3")

def load_test_resources_file():
    bucket_name = os.environ.get("MyBucketName", "my-bucket-1fc71d36")
    key = "cedar_test_resources.json"
    res = s3.get_object(Bucket=bucket_name, Key=key)
    file_content = res["Body"].read().decode("utf-8")
    return file_content

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

def match_request(policies, event):

    _, resource = extract_method_and_resource(event)
    patterns = { }

    for policy in policies:
        patterns[policy.regex] = policy.resource_endpoint 

    for pattern in patterns.keys():
        result = re.findall(pattern, resource)
        if result:
            return result, patterns[pattern]

    return None, None


def generate_cedar_entities():
    entities = []
    return entities

def generate_cedar_request(policies, event, user):
    method, _ = extract_method_and_resource(event)
    _, resource = match_request(policies, event)

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
    return ""

def evalute_cedar(p, e, r):
    decision = is_authorized(r, p, e)
    return Decision.Allow == decision.decision

def handler(event, context):
    print(event)
    token = event["authorizationToken"]
    try:
        user = jwt.decode(token, "author", algorithms=["HS256"])
        if user is None:
           return json.loads(generate_policy("user", "Deny", event["methodArn"]))
        json_text = load_test_resources_file()
        p = get_all_policies(json_text)
        policies = get_policies(user["id"])
        entities = generate_cedar_entities()
        request = generate_cedar_request(p, event, user)
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
