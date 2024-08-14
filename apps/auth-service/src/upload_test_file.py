import boto3

s3 = boto3.resource("s3")

bucket_name = "MyBucket-ea077d56-dcb6-4ae8-b702-38b616cd102f"
file_path = "./cedar_test_resources.json"
key = file_path.replace("./", "")

s3.upload_file(file_path, bucket_name, key)

