import boto3
from handlers.lib.resource_creation import ResourceAction, get_all_resources, create_policy
from typing import List
from uuid import uuid4 as uuid

table = boto3.resource("dynamodb").Table("PoliciesTable")

with open("./cedar_test_resources.json", "r") as file:
    json_text = file.read()

resource_actions: List[ResourceAction] = get_all_resources(json_text)

policies = []

for resource_action in resource_actions:
    policy = create_policy(resource_action)

    item = {
        "id": str(uuid()),
        "policy_name": resource_action.get_policy_name(),
        "policy_definition": policy,
    }

    table.put_item(Item=item)

