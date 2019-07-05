# Amazon-Rekognition

Using Amazon Rekognition one can detect faces, recognize faces, recognize emotions, detect objects and recognize objects.
In this project you can find above mentioned applications of Amazon Rekognition on video file.For doing this follow the below steps.

First create virtual envirinment in your local system. 
For creating it open your command prompt then 
1) Install virtual environment using command:  **pip install virtualenv**
2) Create the virtual environment: **virtualenv ENV** this will create virtual environment having name ENV. 
3) Activate the virtual environment: **ENV\Scripts\activate**

Below are the links for the same.
https://www.techcoil.com/blog/how-to-create-a-python-3-virtual-environment-in-windows-10/ 

https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/


After running third step you will be inside your virtual env. Now install AWS CLI (command line) into this environment using 
**pip3 install awscli**
Now check version of aws cli using: **aws --version**

Configuring the AWS CLI:

Run **aws configure**

When you type this command, the AWS CLI prompts you for four pieces of information (access key, secret access key, AWS Region, and output format). It will look like 
**AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE**

**AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY**

**Default region name [None]: us-west-2**

**Default output format [None]: json**


Enter your access key Id and Secret acces key and the region in which you want to work.

For more details you can refer: https://docs.aws.amazon.com/cli/latest/userguide/install-windows.html

Now create amazon SNS topic and then Amazon SQS standard queue then Subscribe the queue to the topic and give permission to the Amazon SNS topic to send messages to the Amazon SQS queue. For all these steps refer 
https://docs.aws.amazon.com/rekognition/latest/dg/video-analyzing-with-sqs.html they are very simple to impliment only yiou have to click according to doc.
Now you are ready to work in Amazon Rekognition. 

Put your data into S3 bucket (region of your bucket and the region which you have enterd at the time of aws cli configuartion must be same)


Now for performing above mentioned applications download the code file and keep it in some folder on desktop. 
Using **ENV\Scripts\activate** activate virtual env and then **cd (path to code file)** and then **python (name of codefile.py)**


**Note: detect.py contains all API's **








