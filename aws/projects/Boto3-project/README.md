# Hands-on Boto3, Lambda: Implement EC2 Scheduler & S3 Compliance Checker

Purpose of this hands-on training is to provide additional exposure to Boto3 and Lambda to develop an EC2 Scheduler and S3 compliance validator.  The scheduler will stop instances after hours and restart them at the beggining of the day.  The S3 compliance validator will ensure that all S3 buckets in the account have versioning enabled, to remain compliant with the company's storage policies.  These are practical problems that are faced in organizations today.

## Learning Outcomes

At the end of the this hands-on training, students will be able to:

- create a Lambda function and necessary roles and policies

- be able to use the boto3 SDK, specifically with the 'EC2' resource

- parse json output from AWS using boto3

- write a python script from scratch


## Outline

- Part 1 - Review design and pseudocode for Lambda function

- Part 2 - Create test instances

- Part 3 - Setup your AWS credentials file

- Part 4 - Implement and test the Lambda function

- Part 5 - Deploy the Lambda function

- Part 6 - Create a Lambda role

- Part 7 - Create a CloudWatch scheduled event

- Part 8 - Test your function

- Part 9 - Create test buckets

- Part 10 - Modify to check for S3 buckets with versioning disabled

- Part 11 - Test you code via Visual Studio Code

- Part 12 - Deploy your code via the Lambda console

- Part 13 - Update the Lambda role

- Part 14 - Delete your resources!

## Architecture

![Architecture](./architecture.jpg)

## Application Flow

![Flow](./flow.jpg)

