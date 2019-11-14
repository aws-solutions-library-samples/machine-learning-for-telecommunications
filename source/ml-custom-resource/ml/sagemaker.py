#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################################################################################################
#  Copyright 2018-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                      #
#                                                                                                                    #
#  Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance    #
#  with the License. A copy of the License is located at                                                             #
#                                                                                                                    #
#      http://www.apache.org/licenses/LICENSE-2.0                                                                    #
#                                                                                                                    #
#  or in the 'license' file accompanying this file. This file is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES #
#  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions    #
#  and limitations under the License.                                                                                #
######################################################################################################################

import base64
import logging
import boto3
from custom.custom_base import Custom

log = logging.getLogger()
log.setLevel(logging.INFO)


class Sagemaker(Custom):
    def __init__(self, event, context, config_name, s3_bucket=None, s3_prefix_artifacts=None):
        super().__init__(event, context,s3_bucket,s3_prefix_artifacts)
        self.sage = boto3.client('sagemaker')
        self.s3 = boto3.client('s3')
        self.create_config = event["ResourceProperties"]["CreateConfig"]
        self.s3_prefix_artifacts = s3_prefix_artifacts
        self.s3_bucket = s3_bucket
        self.config_name = config_name

    def __call__(self):
        if self.create_config == "true":
            self.create_lifecycle_config()
            return {'PhysicalResourceId': self.event["LogicalResourceId"]}

    def __delete__(self):
        self.delete_lifecycle_config()

    def base64_encode(self,bucket,key):
        try:
            obj = self.s3.get_object(Bucket=bucket, Key=key)
            encoded = base64.b64encode(obj['Body'].read())
            return encoded.decode('utf-8')

        except Exception as e:
            print(e)
            print(
                'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(
                    self.key, self.bucket))
            raise e

    def create_lifecycle_config(self):
        try:
            bucket = self.s3_bucket
            artifacts = super().get_artifactJson()
            key = "{}/scripts/sagemaker-script/{}".format(self.s3_prefix_artifacts, artifacts['artifacts']['configs']['sagemaker'])

            custom_script = self.base64_encode(bucket,key)
            response = self.sage.create_notebook_instance_lifecycle_config(
                NotebookInstanceLifecycleConfigName=self.config_name,
                OnCreate=[
                    {
                        'Content': custom_script
                    },
                ]
            )

            log.info('Response = %s', response)

        except Exception as e:
            print('An error occurred: {}.'.format(e))
            raise e

        return response

    def delete_lifecycle_config(self):
        try:
            response = self.sage.delete_notebook_instance_lifecycle_config(
                NotebookInstanceLifecycleConfigName=self.config_name
            )
            log.info('Response = %s', response)
        except Exception as e:
            print('No Config or An error occurred: {}.'.format(e))
            raise e

