import boto3

def create_item(table_name, item):
    return boto3.resource("dynamodb").Table(table_name).put_item(Item=item)
