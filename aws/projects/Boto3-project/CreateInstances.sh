#For Creating Server with Start/Stop Time Tag

aws ec2 run-instances --instance-type t2.micro --count 3 --key-name <YOUR_KEY_NAME WITHOUT .PEM > --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=<YOUR_NAME>-scheduled-server},{Key=SchedulerStartTime,Value=08-30},{Key=SchedulerStopTime,Value=17-30}]" --image-id $(aws ssm get-parameters --names "//aws\service\ami-amazon-linux-latest\al2023-ami-kernel-default-x86_64" --region us-east-1 --query "Parameters[0].Value" --output text) 

#For Creating Server without Start/Stop Time Tag

aws ec2 run-instances --instance-type t2.micro --count 2 --key-name <YOUR_KEY_NAME WITHOUT .PEM > --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=<YOUR_NAME>-no-scheduled-server} --image-id $(aws ssm get-parameters --names "//aws\service\ami-amazon-linux-latest\al2023-ami-kernel-default-x86_64" --region us-east-1 --query "Parameters[0].Value" --output text) 