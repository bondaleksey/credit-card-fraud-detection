import boto3
from botocore.exceptions import ClientError


session = boto3.session.Session()
s3 = session.client(service_name="s3", endpoint_url="https://storage.yandexcloud.net")

response = s3.list_buckets()
# Output the bucket names
print("Existing buckets:")
for bucket in response["Buckets"]:
    print(f'  {bucket["Name"]}')


s3.upload_file("scripts/test_file.txt", "bond-ccfd", "test/t_file.txt")
try:
    response = s3.upload_file(
        "scripts/test_file.txt",
        "bond-ccfd",
        "test/t_file2.txt",
        ExtraArgs={"ACL": "public-read"},
    )
    # s3_client.upload_file(file_name, bucket, object_name)
except ClientError as e:
    print(e)

print("try to download file")
try:
    s3.download_file("bond-ccfd", "test/t_file.txt", "scripts/downloaded_file.txt")
except ClientError as e:
    print(e)
