import boto3
import os

db = boto3.resource("dynamodb")
policy_assignments_table = db.Table(os.environ["PolicyAssignmentsTableName"])
users_table = db.Table(os.environ["UsersTableName"])
users_roles_table = db.Table(os.environ["UsersRolesTableName"])
roles_permissions_table = db.Table(os.environ["RolesPermissionsTableName"])

def get_user_policies(user_id):
    policies = []
    try:
        # check in the policy assignments table
        response = policy_assignments_table.query(
            IndexName="entityIdEntityTypeIndex",
            KeyConditionExpression=boto3.dynamodb.conditions.Key("entityId").eq(user_id) &
                                   boto3.dynamodb.conditions.Key("entityType").eq("User")
        )

        items = response.get("Items", [])
        for item in items:
            policies.append(item.get("policyId"))

        # get all the user's roles
        users_roles = users_roles_table.query(
            IndexName="userIdIndex",
            KeyConditionExpression=boto3.dynamodb.conditions.Key("userId").eq(user_id)
        ).get("Items", [])

        roles = [i.get("roleId") for i in users_roles]

        # get all the role's permissions
        permissions = []
        for role in roles:
            role_permissions = roles_permissions_table.query(
                IndexName="roleId",
                KeyConditionExpression=boto3.dynamodb.conditions.Key("roleId").eq(role)
            ).get("Items", [])
            for role_permission in role_permissions:
                permissions.append(role_permission.get("permissionId"))

        # finally, get all the policies that are linked to the permissons
        for perm in permissions:
            perm_policies = policy_assignments_table.query(
                IndexName="entityIdEntityTypeIndex",
                KeyConditionExpression=boto3.dynamodb.conditions.Key("entityId").eq(perm) &
                                       boto3.dynamodb.conditions.Key("entityType").eq("Permission")
            ).get("Items", [])
            for p in perm_policies:
                policies.append(p.get("policyId"))


    except Exception as e:
        print(e)
    return policies
