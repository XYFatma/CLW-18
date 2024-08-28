
# Hands-on CodePipeline-01 : Creating and CI/CD Pipeline via AWS CodePipeline

Purpose of the this hands-on training is to create CI/CD Pipeline for Angular App with AWS CodePipeline 

## Learning Outcomes

At the end of the this hands-on training, students will be able to;

- understand what is the CI/CD Pipeline

- demonstrate their knowledge on how to creating CI/CD Pipeline.

- create S3 bucket fpr deployment.

- use GitCommit for version control system-git and create Repository 

- use CodeBuild to build Angular project

- using buildspec.yml file

- using test phases for Angular project via Codebuild and integrate to the CodePipeline project

## Outline
- 

- Part 1 - Creating a Bucket for deployment 

- Part 2 - Creating CodeCommit repository and provide integration with local

- Part 3 - Create CodePipeline

- Part 4 - Integrate Testing to CodePipeline



# PART 1 - Creating a Bucket and Route 53 record for deployment 

## Section 2: Create Bucket 
- Create a bucket with following properties, 

```text
Bucket name                 : myangular.<domainname>
Region                      : N.Virginia
Object Ownership            : ***ACLs enabled - Bucket owner preferred 
Block all public access     : UnChecked (Public)
Versioning                  : Disabled
Tagging                     : 0 Tags
Object-level logging        : Disabled

```

- After creation open the bucket and set "Static WebHosting"

- Click on PROPERTIES  >>>>> STATIC WEBSITE HOSTING >>>> Edit

```text
Static website hosting      : Enable 
Hosting type                : Host a static website
Index document              : index.html
Error document - optional   : index.html
```

- then copy the static Webhosting URL 

## Section 2: Create Record

- Go to Route 53 service

- Create Alias record for S3 bucket

```text
Subdomain   : myangular.<domainname>
RecordType  : A
Alias       : Enabled
Value       : S3 bucket - myangular.<domainname>
TTL         : 60
```

# PART 2 - Creating CodeCommit repository and provide integration with local


## Section 1: Creating CodeCommit repository

- Go to the CodeCommit and click on "Create repository"
- Repository settings

```
Repository name         : xxxxxxmyangularproject2023
Description - optional  :-
Enable Amazon CodeGuru Reviewer for Java and Python - optional: Keep it as is
```
- Click create. 


## Section 2: Integration with local

### Step1: 

- First get Codecommit credentials from IAM
- Go to IAM and Click "Users >>>>> Select user---->>Security Credential--->> HTTPS Git credentials for AWS CodeCommit"

- Click on "Generate credentials"
- Download the .csv file . 
- We'll use this credentials while integrating CodeCommit to your local.

### Step2: 

- to clone your repository to your local computer go to CodeCommit 

- click on newly created repo

-  copy the code like below 

```bash
git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/my-angular-project
```
- open "desktop" of your local via gitbash/terminal
- run the command that you copied before

```bash
git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/my-angular-project
```
- enter your CodeCommit username and password created in Step1

```
  username : your GitCommit username defined in .csv file
  password : your GitCommit password defined in .csv file
```
- your repo will be copied as "my-angular-project" on your local but it will be empty for now.

<!-- - Other option for coping git repo

```
git status
git init
git add .
git commit -m "first commit" 
git remote add origin https://git-codecommit.us-east-1.amazonaws.com/v1/repos/xxxxx-my-angular-project-xxxxxxxxxxxx
git push --set-upstream origin main
  - username : your GitCommit username defined in .csv file
  - password : your GitCommit password defined in .csv file -->
<!-- ``` -->
### Step3: (copy the files from aws clarusway repo to "my-angular-project" folder )

- open the clarusway-aws-xxx folder in your local  "aws/hands-on/CodePipeline_S3_AWS"
- Copy the files inside the folder of "aws/hands-on/CodePipeline_S3_AWS"
- Paste the files into the "my-angular-project" folder in your local
- open "my-angular-project" folder via gitbash/terminal
- then execute the following commands (While pushing to files to CodeCommit it requires username and password)

```
git status
git add .
git commit -m "first commit"
git push
```
- then check your repository 

# PART 3 - Create CodePipeline

### Step1: 

- Go to the CodePipeline menu
- Click on Create Pipeline 

- Choose pipeline settings:
```
Pipeline name       : My first Pipeline
Pipeline type       : V1***
Execution mode      : Superseded 
Service role        : Keep it as is
Allow AWS CodePipeline to create a service role so it can be used with this new pipeline: Enable 
Advanced settings   : Keep it as is
Next
```


- Add source stage:
```
Source provider     : CodeCommit

Repository name     : Your repository name

Branch name         : main 

Change detection options : Keep it as is
  -  Amazon CloudWatch Events (recommended) 
  -  CodePipeline default
```

- Add Build Stage: 

```
Build provider     : AWS CodeBuild
Region             : N.Virginia
Project name       : Click on "Create Project"  and on the opening page 

    - Project name                              : 
    - Description - optional                    : 
    - Enable concurrent build limit - optional  : 
    - Environment image                         : Keep it as is - Managed
    - Operating system                          : Ubuntu
    - Runtime(s)                                : Standard
    - Image                                     : 5.0
    - Image version                             : Keep it as is
    - Environment type                          : Keep it as is- linux 
    - Privileged                                : Keep it as is -Unchecked
    - Service role                              : Keep it as is
    - Build specifications                      : ***Uses a buildspec file
    - Buildspec name - optional                 : Keep it as is - Empty
    - Log                                       : Keep it as is - Empty

    Click on "Continue to Codepipeline" >>> this will direct you to the CodePipeline page again

- Environment variables - optional : Keep it as is
- Build type                       :  Keep it as is

```


- Deployment settings : 

```
- Deploy provider               : AWS S3 
- region                        : N.Virginia
- Bucket                        : your bucket name - myangular.<domainname>
- S3 object key                 : keep it as is --Empty 
- Extract file before deploy    : Enable !!!
- ***Additional configuration      :    

    - KMS encryption key ARN        : keep it as is --Empty 
    - Canned ACL - optional         : "Public read" !!!!!
    - Cache control - optional      : keep it as is --Empty 

```
- create pipeline
- navigate to Pipeline menu and Show the menu 
- Show the website after pipeline is ready 

### Step2 (triger pipeline)

- Go to the "my-angular project" in you local and open  "src>>>  app >>> app.component.html"

- Change "Version 1" as "Version 2 " and save 

- Open the git terminal and commit the new changes to CodeCommit 
```
git status
git add .
git commit -m "second commit" 
git push
```
- then check the pipeline and new version of the project for browser

# PART 4 - Integrate Testing to CodePipeline

### Step1:

- Go to the "my-angular project" in you local and open  `src`>>>  `calculatator` >>> `calculator.component.spec.ts` and "calculator.component.ts"

- Show the unit test 

- Add testing your CodePipeline

- Click on you pipeline >>> Edit 

- Click on "Edit stage" of the "Edit: Build" section

- Click "Add action group" located at the top of the "Build" part - !!!!!!since we click top of this process it will be executed before build stage. !!!!!

- on th opening page 

```
Edit action         : osvaldo_add_test
Action provider     : AWS Codebuild
Region              : N.Virginia
Input artifacts     : SourceArtifact
Project name       : Click on "Create Project"  and on the opening page 

    - Project name                              : 
    - Description - optional                    : 
    - Enable concurrent build limit - optional  : 
    - Environment image                         : Keep it as is - Managed
    - Operating system                          : Ubuntu
    - Runtime(s)                                : Standard
    - Image                                     : 5.0
    - Image version                             : Keep it as is
    - Environment type                          : Keep it as is- linux 
    - Privileged                                : Keep it as is -Unchecked
    - Service role                              : Keep it as is
    - Buildspec   !!!!!!!                       : unit-test-buildspec.yml     !!!!!!!!!!!!!
    - Buildspec name - optional                 : Keep it as is - Empty
    - Log                                       : Keep it as is - Empty

    Click on "Continue to Codepipeline" >>> this will direct you to the CodePipeline page again 

- Environment variables - optional : Keep it as is
- Build type                       :  Keep it as is
```

- Click on  Done and Save 

- Check the Pipeline

- Since we don' have "unit-test-buildspec.yml" we'll get failure 

- So add "unit-test-buildspec.yml" to the under root of myangular project folder . If you don't add it under the root Codepipeline can not find the file.

- 
```
git status
git add .
git commit -m "add test specfile" 
git push
```
- then check the pipeline and new version of the project for browser


### Step2:

- Change the file in the  "my-angular project" open >>> `src`  >>>  `calculater` >>> `calculator.component.spec.ts`

-  in line 55 >>>>> change `expect(component.result).toBe(3);` as `expect(component.result).toBe(4)`. So while testing application will divide 6 by 3 and it will expect `4` as a result rather than `3`. It causes the test to be considered as a failed. 

- save and push the change to the repository

```
git status
git add .
git commit -m "add test failure" 
git push
```
- show that test is failed

- Show that since the test is failed new version is not released and you existing version is still working. 


- Correct the  fault on the "my-angular project" open >>> "src  >>>  calculate >>> `app.component.spec.ts` in  `line 55` as `expect(component.result).toBe(3)`

- then push the new version again 

```
git status
git add .
git commit -m "correction test" 
git push
```
- Show the last version of the page

- Delete the resources : 

 - delete the pipeline

 - delete the build projects - 2 of them

 - delete the CodeCommit repository

 - Delete if there is any Event in AWS EventBridge

 - Empty your artifact Bucket 

 - Empty your  WebHosing bucket 



