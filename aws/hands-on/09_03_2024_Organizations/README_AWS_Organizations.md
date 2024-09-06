# Hands-on AWS Organizations 01 : Configuring AWS Organization and using AWS Organization compatible with IAM Identity Center (SSO)

Purpose of the this hands-on training is to provide working with multiple account via "AWS Organization" and creating user via "IAM Identity Center (SSO)"

## Learning Outcomes

At the end of the this hands-on training, students will be able to;

- learn how to set configuration of AWS Organization

- learn how to add multiple account to organization

- learn how to log in newly created account created by AWS Organization

- learn how to use Service Control Policies (SCP) with AWS Organization

- learn how to use tag policies with AWS Organization

- learn how to use IAM Identity Center (SSO) with AWS Organization

- learn how to close an account created by AWS Organization

## Outline

- Part 1 - Creating an Organization and sandbox account

- Part 2 - Basic operations on AWS Organization

- Part 3 - Using SCPs and Tag Policies in AWS Organization 

- Part 4 - Creating an user via IAM Identity Center (SSO)

- Part 5 - Cleaning 


## Part 1 -  Creating an Organization and Sandbox account


- Navigate to the AWS Organization console 

- Click on "Create an Organization"

- You will see the first hierarch page. 

- Explain the Hierarch of organization and left hand pane Services,  Policies, and  Settings

- !!!!! Explain that you can add new account and after the session you can delete newly created account. AWS will delete the account after 90 days. So student may just want to watch hands-on rather than doing together. 


- Click on "Add an Account" (Since Clarusway has already one named sandbox1, just show how to create for students. )


```text

Create an AWS account (checked)
Create an AWS account
    AWS account name                        : sandbox1
    Email address of the account's owner    : xxxxxx@gmail.com 
                                              (!!!!!!The email must be different than the existing accounts's email. Otherwise the request will be refused)
    
    IAM role name                           : Keep it as is

Tag: Skip tagging
```
- BTW email address will be our "root account email" 

- Check your email 

### Step 2 - Login new account

- To login to new account we need at least 2 values - "root account email" and "root password". We have  defined the root account email while creating an account in AWS Organization. but what about root password ???

- Logging a new account is just the same process with "forget your password" .

- First open a new "incognito  window" on browser

- Go to the sign in page of AWS 

- Select root user access, enter you email and click on "forget password" (As an instructor just show how login fist time.)

- Check your email for verification code , click on link or copy/paste it to the browser and define your new password

- Sign in again wth root user  e-mail and newly created password. 

- Since the students will delete the account after lesson we don't need create IAM user.


- We have another method which uses IAM role. (Instructor will use this method )

- Open new incognito browser

- sign in your existing AWS account 

- click on  your user account name right top of the page 

- clik on "switch role"

-  in the opening page 

   ```text
    Account       : sandbox1 account number 
    Role          : OrganizationAccountAccessRole
    Display name  : demo1
    Color         : blue

```
- click on Switch role

- Now you are login with OrganizationAccountAccessRole . Go to the IAM console and show the OrganizationAccountAccessRole's Policy "AdministratorAccess"
   

## Part 2 - Basic operations on AWS Organization

### Step 1 - Creating an Organizational Unit 

- On Organizational Structure click on "root"

- From the  "Action" menu  select "create new " under the "Organizational Unit "  section

```text
Details
    Organizational unit name: TeamA

Tags: Leave it as is
```
- click on "sandbox1" account from Organizational Structure and then click on "Action menu"

- Select "Move" under the "AWS account " section
```
Destination >> TeamA
```
- Show the Organizational structure again. 

### Step 2 - Creating SPCs to Require Amazon EC2 instances to use a specific type 

- Click on "Policies" from left hand pane

- Click on SCPs 

- Enable SCPs 

- Click on "Create Policy"

- Policy named:  "t2.micro" 

- Policy statement : 

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RequireMicroInstanceType",
      "Effect": "Deny",
      "Action": "ec2:RunInstances",
      "Resource": [
        "arn:aws:ec2:*:*:instance/*"
      ],
      "Condition": {
        "StringNotEquals": {
          "ec2:InstanceType": "t2.micro"
        }
      }
    }
  ]
}
```
- Select newly created policy named "t2.micro" and click on "Action >>> Attach "

- Select OU of "TeamA" and click on "Attach Policy"

- Navigate to the "sandbox1" account to test the policy 

- Go to EC2 service  

- Try to create  EC2 with "t2.medium" instance type

-  You'll get such an error: 

```
Instance launch failed : You are not authorized to perform this operation. Encoded authorization failure message: 
```

### Step 3 - Creating  SCPs to Prevent Amazon S3 unencrypted object uploads

- Create a policy to Prevent Amazon S3 unencrypted object uploads

- Click on "Policies" from left hand pane

- Create policy named "S3" including policy statement seen below 

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "s3:PutObject",
      "Resource": "*",
      "Condition": {
        "Null": {
          "s3:x-amz-server-side-encryption": "true"
        }
      }
    }
  ]
}
```

- Select newly created policy named "S3" and click on "Action >>> Attach "

- Select OU of "TeamA" and click on "Attach Policy"

- To test SCP,  go to s3 services of "sandbox1 " account 

- create an bucket named >>>> yournameawsorganizationscp

- try to upload something that is not encrypted 

- You'll get the error message seen below: 
```
Upload failed : 
View details below.
```
- Delete the bucket

### Step 4 - Using Tag Policies


- Click on "Policies" from left hand pane

- Click on "Tag Policy"

- Enable "Tag Policy"

- Click on  Create "Tag Policy" :

- 
```
Details
Policy name         : mytagpolicy
Policy description - optional

Tags: Skip this part

Visual Editor
Tag key : Department
  Tag key options:
    Tag key capitalization compliance : Checked
    Tag value compliance              : Checked >>>>> Specify values >>> aws,  devops >>>           
                                                                                    save changes

    Resource types to enforce         : Checked >>>>> Specify resource types >>> Dynamodb >>>  
                                                                                    save changes
```
- Create Policy 

- Select newly created policy named "mytagpolicy" and click on "Action >>> Attach "

- Select OU of "TeamA" and click on "Attach Policy"

- To test Tag Policy,  go to DynamoDb services of "sandbox1 " account 

- create an DynamoDB  table name    >>>> yournamedb
                      partition key >>>  id
                      tag           >>>  Key:Department ; Value: Fullstack


- You'll get the error message


- ## Part 4 - Creating an user via IAM Identity Center (SSO)

### Step 1 - Enable IAM Identity Center

- Go to IAM Identity Center service

- click "Enable" button from the right top of the page

- If you can't find this button >>> navigate to "AWS Organization >>Service>>IAM Identity Center" than enable

- !!!! To signin easily, you need to change MFA policy for this service
- Click "Settings " from left hand menu than >>> choose  "Authentication" and >>>  Multi-factor authentication >>> Configure

    - Choose "Never (disabled)" and save 

### Step 2 - Creating an user


- Navigate to IAM Identity Center (successor to AWS Single Sign-On) and Enable the service.

- From the left hand menu click "Users"

- Click "Add user"

- Primary information: 

```
Username            : demo-user
Password            : select "Generate a one-time password that you can share with this user".
Email address       : xxxxx@gmail.com
First name          : xxxx
Last name           : xxxx
Display name        : xxxxx
```
- Keep the other option as is

- Add user to groups - optional >>>> skip this part

- Review and add user.

- Copy the "One-time password" information

- click the newly created user

- on the top of the page you'll see "Primary email not verified" notification. CLick on 
"Send email verification link " too verify your e-mail. 

- go to your e-mail and verify the user . 

- Also  click  "Accept invitation" mail


- Then click "sign in" to access AWS

- Define your new creadetials and log in

- Since you don't have any permission, you'll see nothing .

### Step 3 - Creating an permission set  and assigning it to user for sandbox1 account

- Turn back to "IAM Identity Center console" >>>>> click "Permission sets"

- Click "Create permission set"

```
Permission set type                     : Predefined permission set
Policy for predefined permission set    : ViewOnlyAccess
```
- Click "Next " to set Permission details: 

```
Permission set name     : myViewOnlyAccess
Description             : keep it as is
Session duration        : 2 hour 
Relay state - optional  : keep it as is
```

- Review and create

- Click "AWS accounts" from left hand pane

- Select "sandbox1" >>>> click "Assign users or groups" >>> Users >>> demo-user >>> myfirstViewOnlyAccess >>> Submit

- then log in again as "demo-user" from the incognito window 

- try to create s3 bucket. Since you only have ViewOnlyAccess you are not able create, delete any resources. 

### Step 4 - Creating an permission set (PowerUserAccess) and assigning it to user for your existing account 

- Turn back to "IAM Identity Center console" >>>>> click "Permission sets"

- Click "Create permission set"

```
Permission set type                     : Predefined permission set
Policy for predefined permission set    : PowerUserAccess
```
- Click "Next " to set Permission details: 

```
Permission set name     : myPowerUserAccess
Description             : keep it as is
Session duration        : 2 hour 
Relay state - optional  : keep it as is
```

- Review and create

- Click "AWS accounts" from left hand pane

- Select <your existing account> >>>> click "Assign users or groups" >>> Users >>> demo-user >>> myPowerUserAccess >>> Submit

- then log in again as "demo-user" from the incognito window 

- try to create s3 bucket. Since you only have PowerUserAccess this time  you are able create, delete any resources. 




- ## Part 5 - Cleaning 

- IAM Identity Center

```
Click "Permisson set " >>> myfirstViewOnlyAccess >>> Detach policy
Click "Permisson set " >>> myPowerUserAccess >>> Detach policy

Delete >>>demo-user
```

- Delete organization unit  
   Go to  organizations hierarchy and click on "sandbox1" and move it to out of "TeamA " organization unit 
   Click on "TeamA " organization unit and Delete it 

- Delete sandbox account 

  Go "sandbox1" account and delete the resource if still exist such as S3 or DynamoDB table.
  On AWS organizations page click "sandbox1"
  On top of the page you'll see "Close" (!!!!!As for instructor please do not delete sandbox1 account.)
  Click "Close" and check the conformation boxes. 

- After 90 days the account will ultimately closed.