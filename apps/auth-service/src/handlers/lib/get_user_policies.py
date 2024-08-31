import boto3
import os
import re
from boto3.dynamodb.conditions import Key

from .table import table

def get_user_policies(user_id):
    policies = []
    try:
        # check in the policy assignments table
        response = table.query(
            IndexName="GSI1",
            KeyConditionExpression=Key("GSI1").eq(user_id) & Key("pk").begins_with("POLASSIGN#")
        )

        items = response.get("Items", [])
        print(f"assignments = {items}")
        for item in items:
            policies.append(item.get("policyId"))

        # get all the user's roles
        users_roles = table.query(
            IndexName="GSI1",
            KeyConditionExpression=Key("GSI1").eq(user_id) & Key("pk").begins_with("USERSROLES#")
        ).get("Items", [])

        roles = [i.get("roleId") for i in users_roles]

        # get all the role's permissions
        permissions = []
        for role in roles:
            role_permissions = table.query(
                IndexName="GSI1",
                KeyConditionExpression=Key("GSI1").eq(role) & Key("pk").begins_with("ROLESPERMS#")
            ).get("Items", [])
            for role_permission in role_permissions:
                permissions.append(role_permission.get("permissionId"))

        # finally, get all the policies that are linked to the permissons
        for perm in permissions:
            perm_policies = table.query(
                IndexName="GSI1",
                KeyConditionExpression=Key("GSI1").eq(perm) & Key("pk").begins_with("POLASSIGN#")
            ).get("Items", [])
            for p in perm_policies:
                policies.append(p.get("policyId"))


    except Exception as e:
        print(e)

    # finally, after everything is done, get the policy definitions
    policy_defs = []
    for policy_id in policies:
        policy = table.get_item(Key={"pk": policy_id.strip()})
        item = policy.get("Item", {"policy_definition": ""})
        policy = item.get("policy_definition", "")
        policy_defs.append(policy)
    print(f"policy defs = {policy_defs}")
    return policy_defs

