## Part 1 - Launch an Application

- First download the php-v1.zip, php-v2.zip, php-v3.zip and php-v4.zip files from GitHub and share them via Slack.

- Go to `Elastic Beanstalk` service on AWS console.

- Click `Create Application`.

- Keep `Web server environment`. 

- Enter your application name `MySampleApp`.  (You can also add Application tags if you need.)

- Keep `MySampleApp-env` for the Environment name.

- Select `PHP` for Platform, `PHP 8.1 running on 64bit Amazon Linux 2` for Platform Branch and `(Recommended)` for Platform Version.

- Select `Upload your code` for Application code and select `Local file`.

- Type `mysampleapp-source-v1` for Version label. Then click choose file and upload php-v1.zip file.

- Select `High availability` for `Presets` and hit `Next`.

- For Service Role `Create and use new service role`, then select your EC2 Key Pair, for `EC2 instance profile` go to IAM and create
a new role named `aws-elasticbeanstalk-ec2-role` with the policies below. While creating role choose `EC2`as trusted service, refresh roles, select the new role and hit `Next`.
  - AWSElasticBeanstalkWebTier
  - AWSElasticBeanstalkWorkerTier
  - AWSElasticBeanstalkMulticontainerDocker

- Keep optional `Set up networking, database, and tags` settings default and hit `Next`.

- Remove `t3.micro` , `t3.small` and select `t2.micro` for Instance types under `Capacity`, keep other setting default and hit `Next`.

- Keep optional `Configure updates, monitoring, and logging` settings default and hit `Next`.

- Review and Click `Submit`.

- Wait for Elastic Beanstalk to create the environment for the application. Show the resources being created and listed on the console.

- After the creation of the environment click the link (Application URL) and show the Web Page.

- From the left-hand menu show the app and env menus, talk about them. Click on the tabs like `Configuration`, `Monitoring` etc. and explain them.

- On AWS console and show the resources (Instances, Load Balancers, ASG, CloudFormation, S3 bucket etc.) created by Elastic Beanstalk.

- Show that even you copy and paste the public IP of the instace created by EB nothing happened in browser. Explian the security group and source part of it. 

## Part 2 - Update the Application

- Explain the deployment policies:

https://blog.shikisoft.com/which_elastic_beanstalk_deployment_should_you_use/

### Step 1 - Update the Application - All At Once

- Go to `Elastic Beanstalk` service on AWS console.

- Click `Mysampleapp-env` on the left hand menu, and click `Upload and deploy` to update the application. (You can also click `Application versions` on the left hand menu, and then click `Upload` to update but you have to deploy it manually)

```bash
- Choose file           : php-v2.zip
- Version label         : mysampleapp-source-v2

- Deployment Preferences :

    - Deployment policy   : All At Once
    - Healthy threshold   : OK
    - Ignore health check : False
```
- Wait for Elastic Beanstalk to update the application.

- After the update completed click the link (Application URL) and show the Updated Web Page.

- Click `Mysampleapp` >> `Application versions` and show we have one app but two versions.

### Step 2 - Update the Environment Configuration - Change Capacity 

- From the left hand menu, go to the `Mysampleapp-env` and select `Configuration` and in the opening page select `Capacity` and hit `Edit` to change autoscaling group metrics. Change min. instance number from 1 to 2. 

```bash
Instances Min: 2
          Max: 4 
```
### Step 3 - Update the Application - Rolling

- Click `Mysampleapp-env` on the left hand menu, and click `Upload and deploy` to update the application. 

```bash
- Choose file           : php-v3.zip
- Version label         : mysampleapp-source-v3

- Deployment Preferences :

    - Deployment policy   : Rolling
    - Healthy threshold   : OK
    - Ignore health check : False

```

- Monitor `Events` and `Health` to show the instances updated one by one.

- During the update check the link (Application URL) and show v2 and v3 Web Pages.

- Click `Mysampleapp` >> `Application versions` and show we have one app but 3 versions.


### Step 4 - Update the Application - Rolling with Additional Batch

- Click `Mysampleapp-env` on the left hand menu, and click `Upload and deploy` to update the application. 

```bash
- Choose file           : php-v4.zip
- Version label         : mysampleapp-source-v4

- Deployment Preferences :

    - Deployment policy   : Rolling with Additional Batch
    - Healthy threshold   : OK
    - Ignore health check : False
```
- Show one more instance has been launched as the additional batch.

- Monitor `Events` and `Health` to show the instances updated.

- During the update check the link (Application URL) and show v3 and v4 Web Pages.

- Show one of the first instances has been terminated to come back to the initial capacity. 

## Part 3 - Terminate the Environment

### Step 1 - Terminate the Environment

- Go to `Elastic Beanstalk` service on AWS console.

- Click `Mysampleapp-env` on the left hand menu, from the Actions select `Terminate environment`. (You can also click `Environments` on the left hand menu, select `Mysampleapp-env` and then from the Actions select `Terminate environment` to delete AWS resources.)

- Read the confirmation message and type the name of the environment into the box and click `Terminate`.

- Wait for Elastic Beanstalk to terminate the environment and show events in `Recent events`.

### Step 2 - Restore Environment

- Click `Environments` on the left hand menu, select terminated `Mysampleapp-env` and then from Actions menu select `Restore`.
  `(The terminated environment will remain visible for about an hour.)`

- Show the environment is deployed and working again. 

### Step 3 - Delete Application

- Click `Applications` on the left hand menu, select `MySampleApp`. From `Actions` menu select `Delete application`. Enter the name of the application to confirm and click `Delete`.

- Wait for a while and show both the environment and the application is deleted.