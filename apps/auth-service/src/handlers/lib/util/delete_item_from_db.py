import boto3

def delete_item_from_db(table_name, partition_key):
    table = boto3.resource("dynamodb").Table(table_name)
    return table.delete_item(item={"id": partition_key})
