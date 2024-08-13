# Storing Database Credentials in AWS Secrets Manager.


Purpose of the this hands-on training is to show how to store database credentials securely via AWS Secrets Manager.
 

## Learning Outcomes

At the end of the this extra hands-on training, students will be able to;

- use RD with Flask



## Outline

- Part 1 - Create resources

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

## Part 2 -
- Create if you don't have any EC2 instance. 


    Instance        : `t2.micro`
    Image           : `Amazon 2023 AMI`
    Security Group  : `SSH+ HTTP+ 8080 >>>>.0.0.0.0/0`

- Connect to EC2 instance (If you use VsCode remote SSH don't forget to install Python Extension)

- Install the dependency 

```
sudo dnf update -y
sudo dnf install python3 -y
sudo dnf install python-pip -y
sudo pip3 install Flask==2.3.3
pip3 install flask-mysql
sudo dnf install git -y
```

- Upload the `templates` folder and `app-with-mysql.py` 

```
git clone [your public repo]
```
- open the `app-with-mysql.py` 

- Run the code and show the connection between RDS database and Flask

- http://<PublicIpofınstance>:8080

- Terminate the Instance and the Secret