import boto3

# Create an S3 resource
s3 = boto3.resource('s3')

# Specify the bucket name
bucket_name = 'aslan-boto3-bucket'

# Access the S3 bucket
bucket = s3.Bucket(bucket_name)

# List object in the bucket
for object in bucket.objects.all():
    print('Object key:', object.key)