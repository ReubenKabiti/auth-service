import boto3
import os

db = boto3.resource("dynamodb")
policy_assignmets_table = db.Table(os.environ["PolicyAssignmentsTableName"])

def get_user_policies(user_id):
    policies = []
    try:
        # check in the policy assignments table
        response = policy_assignmets_table.query(
            IndexName="entityIdEntityTypeIndex",
            KeyConditionExpression=boto3.dynamodb.conditions.Key("entityId").eq(user_id) &
                                   boto3.dynamodb.conditions.Key("entityType").eq("User")
        )

        print(response)
        
        items = response.get("Items")
        if not items is None:
            for item in items:
                items.append(item.get("policyId"))

    except Exception as e:
        print(e)
    return policies
