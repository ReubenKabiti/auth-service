from handlers.lib.resource_creation import get_all_policies
from typing import List
from uuid import uuid4 as uuid
import boto3
import os

table = boto3.resource("dynamodb").Table(os.environ.get("TableName", "auth-service-table-dev"))

with open("./cedar_test_resources.json", "r") as file:
    json_text = file.read()

policies = get_all_policies(json_text)

for policy in policies:
    item = {
        "pk": f"POLICY#{str(uuid())}",
        "policy_name": policy.action_name,
        "policy_definition": str(policy),
    }

    table.put_item(Item=item)

