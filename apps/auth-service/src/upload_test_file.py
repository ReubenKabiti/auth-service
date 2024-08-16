import boto3

s3 = boto3.client("s3")

bucket_name = "my-bucket-1fc71d36"
file_path = "./cedar_test_resources.json"
key = file_path.replace("./", "")

s3.upload_file(file_path, bucket_name, key)
