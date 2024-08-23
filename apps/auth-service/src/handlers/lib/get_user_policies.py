import boto3
import os

db = boto3.resource("dynamodb")
policy_assignmets_table = db.table(os.environ["PolicyAssingmentsTableName"])

def get_user_policies(user_id):
    policies = []
    # check in the policy assignments table

    try:
        pass
    except:
        pass
