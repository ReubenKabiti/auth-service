import json

def return_json(body={}, status_code=200):
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
    }

