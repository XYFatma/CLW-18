import boto3
ec2 = boto3.resource('ec2')

# create a new EC2 instance
instances = ec2.create_instances(
     ImageId='ami-0bb84b8ffd87024d8', # ubuntu  ami id
     MinCount=1,
     MaxCount=1,
     InstanceType='t2.micro',
     KeyName='morgoliath-clarusway' #yourkeypair without .pem
 )
