import boto3

stores_table = boto3.resource("dynamodb").Table("StoresTable")

def create_store(params):
    pass

def read_store(store_id):
    response = store_table.get_item(Key={"id": store_id})
    store = response.get("Item")
    return store

def read_stores_from_user(params):
    pass

def update_store(params):
    pass

def delete_store(params):
    pass
