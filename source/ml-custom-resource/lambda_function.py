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

from __future__ import print_function
import os
from data.artifacts import Artifacts
from etl.gluejobs import GlueJobs
from custom import cfn_resource
from ml.sagemaker import Sagemaker

handler = cfn_resource.Resource()

sb_bucket = os.environ['SB_BUCKET']
s3_bucket = os.environ['S3_BUCKET']
s3_prefix_rawdata = os.environ['S3_PREFIX_RAWDATA']
s3_destination_bucket = os.environ['S3_DESTINATION_BUCKET']
sb_prefix_artifacts = os.environ['SB_PREFIX_ARTIFACTS']
s3_prefix_artifacts = os.environ['S3_PREFIX_ARTIFACTS']
config_name = os.environ['LifeCycleConfigName']
job_name = os.environ['GlueJob']
database = os.environ['Database']
output_path = os.environ['OutputPath']

@handler.create
def lambda_handler(event, context):

    try:

        if "MlArtifactsResource" == event["LogicalResourceId"]:
             artifacts = Artifacts(event, context, s3_bucket, s3_destination_bucket, sb_bucket, sb_prefix_artifacts, s3_prefix_artifacts, s3_prefix_rawdata, output_path)
             artifacts.__call__()
        elif "MlGlueResource" == event["LogicalResourceId"]:
            glue_job = GlueJobs(event, context, job_name, database, s3_prefix_rawdata, s3_bucket, s3_prefix_artifacts, output_path)
            glue_job.__call__()
        elif "MlSagemakerResource" == event["LogicalResourceId"]:
            sagemaker = Sagemaker(event, context, config_name, s3_bucket, s3_prefix_artifacts)
            sagemaker.__call__()

        physical_resource_id = {'PhysicalResourceId': event["LogicalResourceId"]}
    except Exception as e:
        print('An error occurred: {}.'.format(e))
        raise e

    return physical_resource_id


@handler.update
def on_update(event, context):
    return {}


@handler.delete
def on_delete(event, context):
    try:
        if "MlGlueResource" == event["LogicalResourceId"]:
            glue_job = GlueJobs(event, context, job_name)
            glue_job.__delete__()
        elif "MlSagemakerResource" == event["LogicalResourceId"]:
            sagemaker = Sagemaker(event, context, config_name)
            sagemaker.__delete__()

        physical_resource_id = {'PhysicalResourceId': event["LogicalResourceId"]}
    except Exception as e:
        print('An error occurred: {}.'.format(e))
        raise e

    return physical_resource_id
