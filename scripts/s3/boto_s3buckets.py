import boto3
from botocore.exceptions import ClientError


session = boto3.session.Session()
s3 = session.client(service_name="s3", endpoint_url="https://storage.yandexcloud.net")

response = s3.list_buckets()
# Output the bucket names
print("Existing buckets:")
for bucket in response["Buckets"]:
    print(f'  {bucket["Name"]}')

for key in s3.list_objects(Bucket="mlops-data")["Contents"]:
    print(key["Key"])
