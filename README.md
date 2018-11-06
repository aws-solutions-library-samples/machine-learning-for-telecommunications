# AWS Machine Learning for All
Machine Learning for All is a solution that helps data scientists in the industry get started using machine learning to generate insights from their data. The solution provides a framework for an end-to-end machine learning process including ad-hoc data exploration, data processing and feature engineering, and modeling training and evaluation.

## AWS Machine Learning for Telecommunications
Machine learning (ML) helps Amazon Web Services (AWS) customers use historical data to predict future outcomes, which can lead to better business decisions. 

Machine learning techniques are core to the Communications Service Providers (CSPs) industry. CSPs can use ML algorithms to construct and refine mathematical models from their business data, and then use these models to help identify fraudulent use of network services, automate network functions (zero touch), and reduce customer churn. 
AWS offers several machine learning services and tools tailored for a variety of use cases and levels of expertise, however it can be a challenge to understand the mechanics of model training and tuning, identify relevant data features, and design a workflow that can perform complex extraction, transformation, and loading (ETL) activities, and also scale to accommodate large datasets. 
To help customers get started with a machine learning workflow for CSPs use cases, AWS offers the Machine Learning for telecom starter kit solution. This solution uses AWS CloudFormation to deploy a scalable, customizable machine learning architecture that leverages Amazon SageMaker, a fully managed machine learning service, and Jupyter Notebook, an open source web application for creating and sharing live code, equations, visualizations and narrative text. 
The solution package provides a framework for an end-to-end machine learning process including ad-hoc data exploration, data processing and feature engineering, and model training and evaluation. It includes a sample telecom IP Data Record (IPDR) dataset to demonstrate how to use machine learning algorithms to test and train models for predictive analysis in telecom. Customers can use the included models as a starting point to develop their own custom machine learning models, and customize the included notebooks for their own use case.  

# Getting Started
01. Prerequisites

The following procedures assumes that all of the OS-level configuration has been completed. They are:

    AWS Command Line Interface
    Python 3.6
    
The Machine Learning solution is developed with python notebook that runs on Sagemaker using pyspark and python as underlying execution code.    

02. Build the machine learning solution

Clone the machine-learning-for-all-solution from GitHub repository:

git clone https://github.com/awslabs/

03. Build the Machine learning solution for deployment:

chmod +x build-s3-dist.sh
./build-s3-dist.sh $DIST_OUTPUT_BUCKET $TEMPLATE_OUTPUT_BUCKET $VERSION 

04. Upload deployment assets to your Amazon S3 bucket:

aws s3 cp ./dist s3://$DIST_OUTPUT_BUCKET/machine-learning-for-all/latest --recursive --acl bucket-owner-full-control

05. Deploy the Machine-learning-for-all solution:

    From your designated Amazon S3 bucket where you uploaded the deployment assets, copy the link location for the machine-learning-for-all.template.
    Using AWS CloudFormation, launch the machine learning for all solution stack using the copied Amazon S3 link for the machine-learning-for-all.template.

    Currently, the Machine Learning solution can be deployed in the following regions: [ us-east-1, us-east-2, us-west-2, eu-west-1, eu-central-1, ap-northeast-1, ap-northeast-2, ap-southeast-2 ]


Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/asl/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions and limitations under the License.
