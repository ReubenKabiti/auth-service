import boto3
from handlers.lib.resource_creation import get_all_policies
from typing import List
from uuid import uuid4 as uuid

table = boto3.resource("dynamodb").Table("PoliciesTable")

with open("./cedar_test_resources.json", "r") as file:
    json_text = file.read()

policies = get_all_policies(json_text)

for policy in policies:
    item = {
        "id": str(uuid()),
        "action_name": policy.action_name,
        "policy_definition": str(policy),
    }

    table.put_item(Item=item)

