import boto3

s3 = boto3.resource('s3')
bucket = s3.Bucket('aslan-boto3-bucket')
bucket.objects.delete()
