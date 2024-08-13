# Storing Database Credentials in AWS Secrets Manager.


Purpose of the this hands-on training is to show how to store database credentials securely via AWS Secrets Manager.
 

## Learning Outcomes

At the end of the this extra hands-on training, students will be able to;

- use AWS secret manager 

- Implement the AWS secrets manager to Python-Flask code



## Outline

- Part 1 - Create a Secret in AWS Secrets Manager

- Part 2 - Run the the Python code in EC2


## Part 1 - Examine and Run the Sample Web Application with SQLite and database implementation in your Local

- We assume that you have already created an MySQL Database with following attitude.

```
- Engine option         : MySQL
- Version               : 8.0.32
- Template              : Free tier
- DB instance class     : db.t2.micro
- Publicly accessible   : ***Yes
- Master username       : admin
- Master password       : Clarusway_1
- Initial DB name       : clarusway

```
  

- Go to the AWS Secrets Manager

- Click on "Store a new Secret"

    Choose secret type: `Credentials for Amazon RDS database`
    Credentials: 
        - User name: `admin`
        - Password: `Clarusway_1`
    Encryption key: `Keep it as is`
    Database: `Choose the database you created`
    Secret name and description: `aws-flask-demo-credential`

- Keep all settings as default and create Secret.

- Open the secret and retrieve the credentials. 


## Part 2 -  Run the the Python code in EC2

- Create a IAM role for EC2 to retrieve data from AWS Secrets Manager 


Trusted entity type  : `AWS Service`
Use case             : `EC2`
Permissions policies : `SecretsManagerReadWrite`
Role name            : `Secret_Manager_EC2` 



- Create if you don't have any EC2 instance. 


    Instance        : `t2.micro`
    Image           : `Amazon 2023 AMI`
    Security Group  : `SSH + HTTP + 8080 >>>>.0.0.0.0/0`
    IAM Profile     : `Secret_Manager_EC2` 

- If you have already had a EC2 instance check the security group and attach `Secret_Manager_EC2` IAM Role 

- Connect to EC2 instance (If you use VsCode remote SSH don't forget to install Python Extension)

- Install the dependency 

```
sudo dnf update -y
sudo dnf install python3 -y
sudo dnf install python-pip
sudo pip3 install Flask==2.3.3
pip3 install flask-mysql
pip3 install boto3
sudo dnf install git -y
```

- Upload the `templates` folder and `app-with-mysql.py` 

```
git clone [your public repo]
```
- open the `app-with-secret-manager.py` 

- Run the code and show the connection between RDS database and Flask

http://<PublicIpofınstance>:8080

- Terminate the Instance and the Secret