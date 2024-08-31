import boto3
import os

table = boto3.resource("dynamodb").Table(os.environ.get("TableName", "auth-service-table-dev"))
