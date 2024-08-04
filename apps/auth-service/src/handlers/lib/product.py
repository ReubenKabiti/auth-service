import boto3

products_table = boto3.resource("dynamodb").Table("ProductsTable")

def delete_product(product_id):
    products_table.delete_item(Key={"id": product_id})

def find_products_from_store(store_id):
    response = products_table.query(
        IndexName="storeId",
        KeyConditionExpression=boto3.dynamodb.conditions.Key("store_id").eq(store_id)
    )

    items = response["Items"]

    return items

