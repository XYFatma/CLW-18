# Hands-on CW-01 : Setting Cloudwatch Alarm Events, and Logging

Purpose of the this hands-on training is to create Dashboard, Cloudwatch Alarm, configure Events option and set Logging up.

## Learning Outcomes

At the end of the this hands-on training, students will be able to;

- create Cloudwatch Dashboard.

- settings Cloudwatch metrics.

- create an Alarm.

- create an Events.

- configure Logging with Agent.


## Outline

- Part 1 - Prep - Launching an Instance

- Part 2 - Creating a Cloudwatch dashboard

- Part 3 - Creating an Alarm

- Part 4 - Creating an Events with Lambda

- Part 5 - Configure Logging with Agent 


## Part 1 - Prep - Launching an Instance

STEP 1 : Create a EC2

- Go to EC2 menu using AWS console

- Launch an Instance
- Configuration of instance.

```text
AMI             : Amazon Linux 2023
Instance Type   : t2.micro
Configure Instance Details:
  - Monitoring ---> Check "Enable CloudWatch detailed monitoring"
Tag             :
    Key         : Name
    Value       : Cloudwatch_Instance 
Security Group ---> Allows ssh, http to anywhere
```
- Set user data.

```bash
#! /bin/bash
dnf update -y
dnf install nginx -y
cd /usr/share/nginx/html
chmod o+w /usr/share/nginx/html
rm index.html
echo "<center> <h1>AWS CloudWatch | Hands-On <h1></center>" > index.html
echo "<center> <h1>The Super Mario Bros. <h1> </center>" >> index.html
echo "<center> <img src="https://assets.nintendo.com/image/upload/f_auto/q_auto/dpr_2.0/c_scale,w_400/E3/2021/Games/M_2_I83iGN8BPSTpu7/mario-party-superstars-switch/description-image" alt="Mario"> <center>" >> index.html
systemctl enable nginx
systemctl start nginx
```


## Part 2 - Creating a Cloudwatch dashboard

- Go to the Cloudwatch Service from AWS console.

- Select Dashboards from left hand pane

- Click "Create Dashboard"
```
Dashboard Name: Clarusway_Dashboard
```

- Select a widget type to configure as "Line"  ---> Next

- Select "Metrics"  ----> Tap configure button

- Select "EC2" as a metrics

- Select "Per-instance" metrics

- Select "Cloudwatch_Instance", "CPUUtilization"  ---> Click "create widget"

- Show EC2 CPUUtilization Metrics.

- Run any of the following two codes.

- 1- install and run the stress tool:

```bash
sudo dnf install stress -y
stress --cpu 80 --timeout 50000
```

- 2- Send an infinite loop of queries to the nginx server 
```bash
while true; do wget -q -O- http://34.204.8.225/; done 
```


## Part 3 - Create an Alarm.

- Select Alarms on left hand pane

- click "Create Alarm"

- Click "Select metric"

- Select EC2 ---> Per-Instance Metrics ---> "CPUUtilization" ---> Select metric

```bash
Metric      : change "period" to 1 minute and keep remaining as default
Conditions  : 
  - Treshold Type                 : Static
  - Whenever CPUUtilization is... : Greater
  - than...                       : 80
```

- click next

```bash
Notification:
  - Alarm state trigger : In alarm
  - Select an SNS topic : 
    - Create new topic
      - Create a new topic: Clarus-alarm
      - Email endpoints that will receive the notification: <your email address>
    - create topic

EC2 action
  - Alarm state trigger
    - In alarm ---> Select "Stop Instance"
```

- click next

- Alarm Name  : My First Cloudwatch Alarm
  Description : My First Cloudwatch Alarm

- click next --- > review and click create alarm

- go to email box and confirm the e-mail sent by AWS SNS

- go to the terminal and connect EC2 instance via ssh

- install and run the stress tool:

```bash
sudo dnf install stress -y
stress --cpu 80 --timeout 50000
```
- Go to dashboard and check the EC2 metrics

- you will receive a alarm message to your email and this message trigger to stop your EC2 Instance.

- go to EC2 instance list and show the stopped instance

- restart this instance.



## Part 4 - Configure Logging with Agent 

STEP 1 : Create second EC2 Instance

- Go to EC2 menu using AWS console

- Launch an Instance
- Configuration of instance.

```text
AMI             : Amazon Linux 2023
Instance Type   : t2.micro
Tag             :
    Key         : Name
    Value       : Cloudwatch_Log
Security Group ---> Allows ssh, http to anywhere
```
- Set user data.

```bash
#! /bin/bash

dnf update -y
dnf install nginx -y
cd /usr/share/nginx/html
chmod o+w /usr/share/nginx/html
rm index.html
echo "<center> <h1>AWS CloudWatch | Hands-On <h1></center>" > index.html
echo "<center> <h1>The Super Mario Bros. <h1> </center>" >> index.html
echo "<center> <img src="https://assets.nintendo.com/image/upload/f_auto/q_auto/dpr_2.0/c_scale,w_400/E3/2021/Games/M_2_I83iGN8BPSTpu7/mario-party-superstars-switch/description-image" alt="Mario"> <center>" >> index.html
systemctl enable nginx
systemctl start nginx 
```

STEP 2 : Create IAM role

- Go to IAM role on AWS console

- Click Roles on left hand pane

- click create role

- select EC2 ---> click next permission

- select "CloudWatchLogsFullAccess"  ---> Next

- Add tags ---> Next

- Review
	- Role Name : Claruscloudwatchlog  
  - Role Description: Clarusway Cloudwatch EC2 logs access role

- click create role

- Go to instance named "Cloudwatch_Log" ---> Actions ---> Security ---> Modify IAM role ---> Attach "CloudWatchLogsFullAccess" role ---> Apply

STEP 3:  Install and Configure the CloudWatch Logs Agent

- Go to the terminal and connect to the Instance named "Cloudwatch_Log"

- Install cloudwatch log agent:
```bash
sudo dnf install amazon-cloudwatch-agent -y
```
- Enable it:
```bash
sudo systemctl enable amazon-cloudwatch-agent
```
- Use config wizard to create the config file:
```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard


```
- You have many options here like creating custom metrics and saving the config file to SSM but for the sake of this handson 
we'll just configure it for the nginx logs.

- Configure as seen below:

```bash
On which OS are you planning to use the agent?
1. linux
2. windows
3. darwin
default choice: [1]: 1

Are you using EC2 or On-Premises hosts?
1. EC2
2. On-Premises
default choice: [1]: 1

Which user are you planning to run the agent?
1. cwagent
2. root
3. others
default choice: [1]: 2

Do you want to turn on StatsD daemon?
1. yes
2. no
default choice: [1]: 2

Do you want to monitor metrics from CollectD? WARNING: CollectD must be installed or the Agent will fail to start
1. yes
2. no
default choice: [1]: 2

Do you want to monitor any host metrics? e.g. CPU, memory, etc.
1. yes
2. no
default choice: [1]: 2

Do you have any existing CloudWatch Log Agent configuration file to import for migration?
1. yes
2. no
default choice: [2]: 2

Do you want to monitor any log files?
1. yes
2. no
default choice: [1]: 1

Log file path: 
/var/log/nginx/access.log

Log group name:
default choice: [access.log]: Enter

Log group class:
1. STANDARD
2. INFREQUENT_ACCESS
default choice: [1]: 1

Log stream name:
default choice: [{instance_id}]: Enter

Log Group Retention in days: 2

Do you want to specify any additional log files to monitor?
1. yes
2. no
default choice: [1]: 1

Log file path:
/var/log/nginx/error.log

Log group name:
default choice: [error.log]: Enter

Log group class:
1. STANDARD
2. INFREQUENT_ACCESS
default choice: [1]: 1

Log stream name:
default choice: [{instance_id}]: Enter

Log Group Retention in days: 2

Do you want to specify any additional log files to monitor?
1. yes
2. no
default choice: [1]: 2

Do you want the CloudWatch agent to also retrieve X-ray traces?
1. yes
2. no
default choice: [1]: 2

Do you want to store the config in the SSM (AWS Systems Manager) parameter store? 
1. yes
2. no
default choice: [1]: 2
```

- Start the agent using the config file:
```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json
```

STEP 4: Get the logs

- Go to the EC2 instance, grab the public IP address and paste it to the browser. Logs should be sent to the cloudwatch logs.

- Go to the Cloudwatch and select Log groups. 

- Select the created log groups named "access.log" and "error.log" ---> Show the created "log streams".


## Part 5 : SNS Topic for Nginx logs

- CloudWatch > Log Groups > Access Log

- Metric Filters > Create Metric Filter

```bash
Filter pattern: [host, logName, user, timestamp, request, statusCode=4*, size]
Select log data to test : i-0418f062d2c4c1fe0 ( ami - change)
Click `Test pattern` button 

Filter name : ERROR
Metric namespace : LogMetrics4XX
Metric name : AccessLog_4XX_Error
Metric value : 1
Review and create > Create Metric Filter

```
- Metric Filters > Create Alarm

```bash
Metric name : AccessLog_Error
Statistic : Sum
Period : 1 minute

Threshold type : Statistic
Whenever AccessLog_Error is... Greater > 5

Alarm state trigger : In Alarm
Slect `Send a notification to the following SNS topic`
Send a notification to… : Default_CloudWatch_Alarms_Topic

Add name and description
Alarm name : Error-404
Alarm description - optional : Nginx - Error- 404
Click `Create Alarm` button 

```