#!/usr/bin/python
# -*- coding: utf-8 -*-

##############################################################################
#  Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.   #
#                                                                            #
#  Licensed under the Amazon Software License (the 'License'). You may not   #
#  use this file except in compliance with the License. A copy of the        #
#  License is located at                                                     #
#                                                                            #
#      http://aws.amazon.com/asl/                                            #
#                                                                            #
#  or in the 'license' file accompanying this file. This file is distributed #
#  on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,        #
#  express or implied. See the License for the specific language governing   #
#  permissions and limitations under the License.                            #
##############################################################################
import json
import boto3


class Custom(object):
    def __init__(self, event, context,bucket=None,prefix=None):
        self.event = event
        self.context = context
        self.physical_resource_id = {'PhysicalResourceId': 'machine-learning-resource'}
        self.bucket = bucket
        self.prefix = prefix
        self.config_file = "ArtifactsConfig.json"

    def read_json(self,bucket,key):
        try:
            obj = boto3.client('s3').get_object(Bucket=bucket, Key=key)
            content = obj['Body'].read().decode('utf-8')
            json_content = json.loads(content)
            return json_content

        except Exception as e:
            print('An error occurred: {}.'.format(e))
            raise e

    def get_artifactJson(self):
        try:
            key = "{}/config/{}".format(self.prefix,self.config_file)
            artifacts_json = self.read_json(self.bucket,key)
            return artifacts_json

        except Exception as e:
            print('An error occurred: {}.'.format(e))
            raise e


