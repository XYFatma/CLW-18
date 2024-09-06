import boto3
ec2 = boto3.resource('ec2')
ec2.Instance('i-095aec48b65874967').terminate() # put your instance id