import boto3

session = boto3.session.Session()

s3 = session.client(service_name="s3", endpoint_url="https://storage.yandexcloud.net")


for key in s3.list_objects(Bucket="mlops-data")["Contents"]:
    print(key["Key"])
    copy_source = {"Bucket": "mlops-data", "Key": key["Key"]}
    s3.copy(copy_source, "bond-ccfd", key["Key"])
    # break
