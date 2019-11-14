# AWS Machine Learning for All

Machine Learning for All is a solution that helps data scientists in the industry get started using machine learning to generate insights from their data. The solution provides a framework for an end-to-end machine learning process including ad-hoc data exploration, data processing and feature engineering, and modeling training and evaluation.

## AWS Machine Learning for Telecommunications
Machine learning (ML) helps Amazon Web Services (AWS) customers use historical data to predict future outcomes, which can lead to better business decisions. 

Machine learning techniques are core to the Communications Service Providers (CSPs) industry. CSPs can use ML algorithms to construct and refine mathematical models from their business data, and then use these models to help identify fraudulent use of network services, automate network functions (zero touch), and reduce customer churn. 
AWS offers several machine learning services and tools tailored for a variety of use cases and levels of expertise, however it can be a challenge to understand the mechanics of model training and tuning, identify relevant data features, and design a workflow that can perform complex extraction, transformation, and loading (ETL) activities, and also scale to accommodate large datasets. 
To help customers get started with a machine learning workflow for CSPs use cases, AWS offers the Machine Learning for telecom starter kit solution. This solution uses AWS CloudFormation to deploy a scalable, customizable machine learning architecture that leverages Amazon SageMaker, a fully managed machine learning service, and Jupyter Notebook, an open source web application for creating and sharing live code, equations, visualizations and narrative text. 
The solution package provides a framework for an end-to-end machine learning process including ad-hoc data exploration, data processing and feature engineering, and model training and evaluation. It includes a sample telecom IP Data Record (IPDR) dataset to demonstrate how to use machine learning algorithms to test and train models for predictive analysis in telecom. Customers can use the included models as a starting point to develop their own custom machine learning models, and customize the included notebooks for their own use case.  

# Getting Started
## Prerequisites
The following procedures assumes that all of the OS-level configuration has been completed. They are:

* [AWS Command Line Interface](https://aws.amazon.com/cli/)
* Python 3.7 or later

The Machine Learning solution is developed with python notebook that runs on SageMaker using pyspark and python as underlying execution code.

## 1. Build the machine learning solution

Clone the machine-learning-for-telecommunications from GitHub repository:

git clone https://github.com/awslabs/machine-learning-for-telecommunications

## 2. Build the machine learning solution for deployment
Build the distributable:
```
DIST_OUTPUT_BUCKET=my-bucket-name # S3 bucket name where customized code will reside
SOLUTION_NAME=my-solution-name
VERSION=my-version # version number for the customized code
INSDUSTRY=telecom
cd ./deployment \n
chmod +x ./build-s3-dist.sh \n
./build-s3-dist.sh $DIST_OUTPUT_BUCKET $SOLUTION_NAME $VERSION $INSDUSTRY \n
```

> **Notes**: The _build-s3-dist_ script expects the bucket name as one of its parameters, and this value should not include the region suffix.

## 3. Upload deployment assets to your Amazon S3 bucket

The CloudFormation template is configured to pull the Lambda deployment packages from Amazon S3 bucket in the region the template is being launched in. Create a bucket in the desired region with the region name appended to the name of the bucket. eg: for us-east-1 create a bucket named: ```my-bucket-us-east-1```.
```
aws s3 cp ./regional-s3-assets/ s3://my-bucket-us-east-1/machine-learning-for-all/$VERSION --recursive --acl bucket-owner-full-control
```

## 4. Upload dataset assets to your Amazon S3 Bucket

This solution includes synthetic demo IP Data Record (IPDR) datasets in Abstract Syntax Notation One (ASN.1) format and call detail record (CDR) format. You can choose to copy these datasets into the source bucket to run the demo of AWS Glue transformations and ML model predictions, or use your own datasets.

In the following example, the dataset is copied from the ```solutions-us-east-1``` S3 bucket to your S3 bucket for your solution named: ```my-bucket-us-east-1```, which also holds your other customized regional code.

```
DIST_OUTPUT_BUCKET=my-bucket-name # S3 bucket name where customized code will reside
SOLUTION_NAME=my-solution-name
VERSION=my-version # version number for the customized code
INDUSTRY=telecom
REGION=us-east-1 # region for S3 buckets for synthetic data

SYNTHETIC_DATASET=s3://solutions-${REGION}/machine-learning-for-all/$VERSION/industry/$INDUSTRY/data
MY_DATASET=${DIST_OUTPUT_BUCKET}-${REGION}/${SOLUTION_NAME}/$VERSION/industry/$INDUSTRY/data

aws s3 cp $SYNTHETIC_DATASET/cdr-start/cdr_start.csv s3://$MY_DATASET/cdr-start/cdr_start.csv --acl bucket-owner-full-control
aws s3 cp $SYNTHETIC_DATASET/cdr-stop/cdr_stop.csv s3://$MY_DATASET/cdr-stop/cdr_stop.csv   --acl bucket-owner-full-control
aws s3 cp $SYNTHETIC_DATASET/cdr-start-sample/cdr_start_sample.csv  s3://$MY_DATASET/cdr-start-sample/cdr_start_sample.csv  --acl bucket-owner-full-control
aws s3 cp $SYNTHETIC_DATASET/cdr-stop-sample/cdr_stop_sample.csv  s3://$MY_DATASET/cdr-stop-sample/cdr_stop_sample.csv  --acl bucket-owner-full-control
```

 > **Notes**: Choose your desired region by changing region in the above example from us-east-1 to your desired region of the S3 buckets.

## 5. Launch the CloudFormation template

* Get the link of the machine-learning-for-all.template uploaded to your Amazon S3 bucket.
* Deploy the Machine Learning solution to your account by launching a new AWS CloudFormation stack using the link of the machine-learning-for-all.template.
* Currently, the Machine Learning solution can be deployed in the following regions: [ us-east-1, us-east-2, us-west-2, eu-west-1, eu-central-1, ap-northeast-1, ap-northeast-2, ap-southeast-2 ]

***

Copyright 2018-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
