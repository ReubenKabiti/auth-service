import boto3

table = boto3.resource("dynamodb").Table("ProductsTable")

def delete_product(product_id):
    table.delete_item(Key={"id": product_id})
